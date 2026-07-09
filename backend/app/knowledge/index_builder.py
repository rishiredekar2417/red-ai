import hashlib
import time
from pathlib import Path

from app.indexer.indexer import ProjectIndexer
from app.knowledge.store import KnowledgeStore
from app.knowledge.embeddings import EmbeddingProvider
from app.knowledge.vector_store import VectorStore
from app.workspace.scanner import WorkspaceScanner


class IndexBuilder:

    def __init__(self, root: Path):

        self.root = Path(root).resolve()

        self.workspace = WorkspaceScanner(self.root)

        self.indexer = ProjectIndexer()

        self.store = KnowledgeStore(self.root)
        # vector store for chunk embeddings
        self.vector_store = VectorStore()
        self.embedding_provider = EmbeddingProvider(dim=32)
        self.vector_path = self.root / "knowledge" / "chunk_vectors.json"
        self.force_vector_regen = False
        if self.vector_path.exists():
            try:
                self.vector_store.load(self.vector_path)
            except Exception:
                # if load fails, start fresh and mark for regen
                self.vector_store = VectorStore()
                self.force_vector_regen = True

    def build(self, force: bool = False):
        start_time = time.time()
        current_files = self.workspace.scan()
        current_paths = {file.path for file in current_files}

        cached_index = self.store.load() if self.store.exists() else []
        cached_by_path = {item["path"]: item for item in cached_index}

        indexed = []
        updated = 0
        removed_files = 0
        removed_vectors = 0
        file_skipped = 0
        chunk_skipped = 0
        indexed_count = 0
        generated = 0
        corrupted = 0

        # Build new index entries and compute desired chunk ids + hashes
        desired_chunk_ids = set()
        desired_chunk_hashes = {}
        reindexed_paths = set()

        for workspace_file in current_files:
            path = Path(workspace_file.path)
            cached_item = cached_by_path.get(str(path))
            should_index = force or self._should_index(path, cached_item, workspace_file)

            if not should_index:
                # file-level skip
                file_skipped += 1
                indexed.append(cached_item)
                # If vector DB was corrupted or missing, regenerate vectors for cached chunks
                if self.force_vector_regen and cached_item is not None:
                    try:
                        for chunk in cached_item.get("chunks", []):
                            chunk_id = f"{cached_item['path']}:{chunk.get('name')}:{chunk.get('start_line')}"
                            ch_hash = hashlib.sha256((chunk.get("content") or "").encode("utf-8")).hexdigest()
                            existing_meta = self.vector_store.meta.get(chunk_id, {})
                            if existing_meta.get("chunk_hash") == ch_hash and chunk_id in self.vector_store.vectors:
                                chunk_skipped += 1
                                continue
                            vec = self.embedding_provider.embed(chunk.get("content", ""))
                            meta = {
                                "path": cached_item["path"],
                                "name": chunk.get("name"),
                                "start_line": chunk.get("start_line"),
                                "end_line": chunk.get("end_line"),
                                "chunk_hash": ch_hash,
                            }
                            self.vector_store.add(chunk_id, vec, meta)
                            # ensure this regenerated chunk is considered desired
                            desired_chunk_ids.add(chunk_id)
                            desired_chunk_hashes[chunk_id] = ch_hash
                            generated += 1
                    except Exception:
                        pass
                continue

            reindexed_paths.add(str(path))
            indexed_file = self.indexer.index_file(path)
            item = self._serialize_indexed_file(indexed_file)
            item["mtime"] = path.stat().st_mtime
            item["size"] = path.stat().st_size
            item["hash"] = self._hash_file(path)

            indexed.append(item)
            # compute chunk hashes and register desired ids
            try:
                for chunk in item.get("chunks", []):
                    content = chunk.get("content", "") or ""
                    ch_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    chunk["chunk_hash"] = ch_hash
                    chunk_id = f"{item['path']}:{chunk.get('name')}:{chunk.get('start_line')}"
                    desired_chunk_ids.add(chunk_id)
                    desired_chunk_hashes[chunk_id] = ch_hash
                    # debug
                    # print(f"DEBUG: desired chunk {chunk_id} hash={ch_hash}")
            except Exception:
                pass
            # For files we re-indexed (force or changed), regenerate their vectors now
            try:
                for chunk in item.get("chunks", []):
                    chunk_id = f"{item['path']}:{chunk.get('name')}:{chunk.get('start_line')}"
                    ch_hash = chunk.get("chunk_hash")
                    # if identical vector exists, skip regeneration
                    existing_vec = self.vector_store.vectors.get(chunk_id)
                    existing_meta = self.vector_store.meta.get(chunk_id, {})
                    if existing_vec is not None and existing_meta.get("chunk_hash") == ch_hash:
                        continue
                    vec = self.embedding_provider.embed(chunk.get("content", ""))
                    meta = {
                        "path": item["path"],
                        "name": chunk.get("name"),
                        "start_line": chunk.get("start_line"),
                        "end_line": chunk.get("end_line"),
                        "chunk_hash": ch_hash,
                    }
                    self.vector_store.add(chunk_id, vec, meta)
                    generated += 1
            except Exception:
                pass
            if force:
                indexed_count += 1
            elif cached_item is None:
                indexed_count += 1
            else:
                updated += 1

        for cached_path, cached_item in cached_by_path.items():
            if cached_path not in current_paths:
                removed_files += 1

        # --- Vector maintenance ---
        # Validate loaded vectors
        try:
            _, corrupted_ids = self.vector_store.validate(self.embedding_provider.dim)
            corrupted = len(corrupted_ids)
        except Exception:
            corrupted = 0

        # Build lookup maps for existing vectors
        existing_meta = dict(self.vector_store.meta)
        existing_ids = set(self.vector_store.vectors.keys())

        # Map by chunk_hash and by (path,start)
        meta_by_hash = {}
        meta_by_pos = {}
        for vid, m in existing_meta.items():
            ch = m.get("chunk_hash")
            if ch:
                meta_by_hash.setdefault(ch, []).append(vid)
            p = m.get("path")
            s = m.get("start_line")
            if p and s is not None:
                meta_by_pos.setdefault((p, int(s)), []).append(vid)

        # For desired chunks: decide skip/update/generate
        for chunk_id in list(desired_chunk_ids):
            desired_hash = desired_chunk_hashes.get(chunk_id)
            # parse chunk id into path, name, start
            parts = chunk_id.rsplit(":", 2)
            pth = parts[0]
            name = parts[1] if len(parts) > 1 else ""
            try:
                start = int(parts[2]) if len(parts) > 2 else 0
            except Exception:
                start = 0

            if chunk_id in existing_ids:
                # present under same id -> verify hash
                meta = existing_meta.get(chunk_id, {})
                if meta.get("chunk_hash") == desired_hash:
                    chunk_skipped += 1
                    continue
                else:
                    # modified chunk: regenerate
                    try:
                        # find corresponding chunk content from indexed list
                        # locate item and chunk
                        parts = chunk_id.rsplit(":", 2)
                        pth = parts[0]
                        name = parts[1] if len(parts) > 1 else ""
                        start = int(parts[2]) if len(parts) > 2 else 0
                        # find in indexed
                        for it in indexed:
                            if it and it.get("path") == pth:
                                for ch in it.get("chunks", []):
                                    if ch.get("start_line") == start and ch.get("name") == name:
                                        vec = self.embedding_provider.embed(ch.get("content", ""))
                                        meta = {
                                            "path": it["path"],
                                            "name": ch.get("name"),
                                            "start_line": ch.get("start_line"),
                                            "end_line": ch.get("end_line"),
                                            "chunk_hash": ch.get("chunk_hash"),
                                        }
                                        self.vector_store.add(chunk_id, vec, meta)
                                        updated += 1
                                        break
                                break
                    except Exception:
                        # fallback: regenerate naive
                        try:
                            vec = self.embedding_provider.embed("")
                            self.vector_store.add(chunk_id, vec, {"chunk_hash": desired_hash})
                            updated += 1
                        except Exception:
                            pass
                    continue

            # not present under same id: try to find by chunk_hash (renamed) or by position
            found = False
            if desired_hash and desired_hash in meta_by_hash:
                # reuse existing vector for this hash
                src_id = meta_by_hash[desired_hash][0]
                src_vec = self.vector_store.vectors.get(src_id)
                src_meta = dict(self.vector_store.meta.get(src_id, {}))
                # copy to new id with updated meta
                parts = chunk_id.split(":")
                pth = ":".join(parts[0:-2]) if len(parts) > 2 else parts[0]
                name = parts[-2]
                start = int(parts[-1])
                new_meta = {
                    "path": pth,
                    "name": name,
                    "start_line": start,
                    "end_line": src_meta.get("end_line"),
                    "chunk_hash": desired_hash,
                }
                self.vector_store.add(chunk_id, src_vec, new_meta)
                chunk_skipped += 1
                found = True
            else:
                # try by position (rename detection)
                pos_key = (pth, start)
                if pos_key in meta_by_pos:
                    src_id = meta_by_pos[pos_key][0]
                    src_vec = self.vector_store.vectors.get(src_id)
                    src_meta = dict(self.vector_store.meta.get(src_id, {}))
                    name = parts[-2]
                    new_meta = {
                        "path": pth,
                        "name": name,
                        "start_line": start,
                        "end_line": src_meta.get("end_line"),
                        "chunk_hash": desired_hash,
                    }
                    self.vector_store.add(chunk_id, src_vec, new_meta)
                    chunk_skipped += 1
                    found = True

            if found:
                continue

            # Otherwise generate new vector
            try:
                for it in indexed:
                    if it and it.get("path") == pth:
                        for ch in it.get("chunks", []):
                            if ch.get("start_line") == start and ch.get("name") == name:
                                vec = self.embedding_provider.embed(ch.get("content", ""))
                                meta = {
                                    "path": it["path"],
                                    "name": ch.get("name"),
                                    "start_line": ch.get("start_line"),
                                    "end_line": ch.get("end_line"),
                                    "chunk_hash": ch.get("chunk_hash"),
                                }
                                self.vector_store.add(chunk_id, vec, meta)
                                generated += 1
                                found = True
                                break
                        break
            except Exception:
                pass

        # Remove vectors that no longer have a corresponding desired chunk
        # Only remove vectors for files that were deleted, or for files we reindexed where chunks disappeared.
        for vid in list(existing_ids):
            meta = existing_meta.get(vid, {})
            mpath = meta.get("path")
            # deleted file
            if mpath not in current_paths:
                self.vector_store.remove(vid)
                removed_vectors += 1
                continue
            # if we reindexed this file, and this vid is not in desired_chunk_ids, it is a deleted chunk
            if mpath in reindexed_paths and vid not in desired_chunk_ids:
                self.vector_store.remove(vid)
                removed_vectors += 1
                continue

        persisted_index = [item for item in indexed if item is not None]
        self.store.save(persisted_index)
        # persist vector index
        try:
            self.vector_store.save(self.vector_path)
        except Exception:
            pass

        elapsed = round(time.time() - start_time, 3)
        # print diagnostics
        print("----------------------------------------")
        print("Vector Index Summary")
        print(f"Generated : {generated}")
        print(f"Updated   : {updated}")
        print(f"Deleted Files : {removed_files}")
        print(f"Deleted Vectors : {removed_vectors}")
        print(f"Skipped Files  : {file_skipped}")
        print(f"Skipped Chunks : {chunk_skipped}")
        print(f"Corrupted : {corrupted}")
        print(f"Total Vectors: {len(self.vector_store.vectors)}")
        print(f"Time      : {elapsed} seconds")
        print("----------------------------------------")

        return {
            "indexed": indexed_count,
            "updated": updated,
            "removed": removed_files,
            "skipped": file_skipped,
            "generated": generated,
            "corrupted": corrupted,
            "total": len(persisted_index),
            "time": elapsed,
        }

        elapsed = round(time.time() - start_time, 3)
        return {
            "indexed": indexed_count,
            "updated": updated,
            "removed": removed,
            "skipped": skipped,
            "total": len(persisted_index),
            "time": elapsed,
        }

    def _serialize_indexed_file(self, indexed_file):
        return {
            "path": indexed_file.path,
            "language": indexed_file.language,
            "size": indexed_file.size,
            "lines": indexed_file.lines,
            "functions": indexed_file.functions,
            "classes": indexed_file.classes,
            "imports": indexed_file.imports,
            "chunks": [chunk.model_dump() for chunk in indexed_file.chunks],
            "function_chunks": [chunk.model_dump() for chunk in indexed_file.function_chunks],
            "class_chunks": [chunk.model_dump() for chunk in indexed_file.class_chunks],
        }

    def _should_index(self, path: Path, cached_item, workspace_file):
        if cached_item is None:
            return True

        if not path.exists():
            return False

        current_stat = path.stat()
        current_mtime = current_stat.st_mtime
        current_size = current_stat.st_size

        cached_mtime = cached_item.get("mtime")
        cached_size = cached_item.get("size")

        if cached_mtime is None or cached_size is None:
            return True

        if current_mtime != cached_mtime or current_size != cached_size:
            return True

        return False

    def _hash_file(self, path: Path) -> str:
        try:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()
        except Exception:
            return ""