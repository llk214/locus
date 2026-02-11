"""
Model management for the Locus application.
Handles FastEmbed model cache discovery, download, deletion, and status checking.
"""

import sys
import os
import tempfile


def get_fastembed_cache_locations():
    """Get FastEmbed cache locations (current + legacy)."""
    locations = []

    env_path = os.environ.get("FASTEMBED_CACHE_PATH")
    if env_path:
        locations.append(env_path)

    temp_dir = tempfile.gettempdir()
    locations.append(os.path.join(temp_dir, "fastembed_cache"))

    if os.name == "nt":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            locations.append(os.path.join(localappdata, "Temp", "fastembed_cache"))
        temp_env = os.environ.get("TEMP", "")
        if temp_env:
            locations.append(os.path.join(temp_env, "fastembed_cache"))

    locations.append(os.path.expanduser("~/.cache/fastembed_cache"))

    seen = set()
    unique_locations = []
    for loc in locations:
        normalized = os.path.normpath(loc)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_locations.append(normalized)

    return unique_locations


BUNDLED_MODEL = "BAAI/bge-small-en-v1.5"


def is_bundled_model(model_name):
    return model_name == BUNDLED_MODEL


def get_bundled_model_path():
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        possible_paths = [
            os.path.join(base_path, '_internal', 'models', 'bge-small-en-v1.5'),
            os.path.join(base_path, 'models', 'bge-small-en-v1.5'),
            os.path.join(os.path.dirname(sys.executable), '_internal', 'models', 'bge-small-en-v1.5'),
            os.path.join(os.path.dirname(sys.executable), 'models', 'bge-small-en-v1.5'),
        ]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, 'models', 'bge-small-en-v1.5'),
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if 'model.onnx' in files or 'model_optimized.onnx' in files:
                    return path
    return None


def is_model_downloaded(model_name):
    if is_bundled_model(model_name) and get_bundled_model_path():
        return True
    
    model_short = model_name.split("/")[-1]
    
    for cache_dir in get_fastembed_cache_locations():
        if not os.path.exists(cache_dir):
            continue
        
        try:
            for folder in os.listdir(cache_dir):
                if model_short in folder or model_short.replace("-", "_") in folder:
                    folder_path = os.path.join(cache_dir, folder)
                    for root, dirs, files in os.walk(folder_path):
                        if 'model.onnx' in files or 'model_optimized.onnx' in files:
                            return True
        except (PermissionError, OSError):
            continue
    
    return False


def verify_model_available(model_name):
    """Verify model is available locally without triggering a download."""
    if is_bundled_model(model_name) and get_bundled_model_path():
        return True, None

    try:
        from fastembed import TextEmbedding
    except Exception as e:
        return False, str(e)

    cache_dir = os.environ.get("FASTEMBED_CACHE_PATH")
    old_offline = os.environ.get("HF_HUB_OFFLINE")
    os.environ["HF_HUB_OFFLINE"] = "1"
    try:
        try:
            model = TextEmbedding(model_name=model_name, cache_dir=cache_dir, local_files_only=True)
        except TypeError:
            model = TextEmbedding(model_name=model_name, cache_dir=cache_dir)
        # This will raise if files are missing
        list(model.embed(["test"]))
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        if old_offline is None:
            os.environ.pop("HF_HUB_OFFLINE", None)
        else:
            os.environ["HF_HUB_OFFLINE"] = old_offline


def get_model_cache_size(model_name):
    """Get cached model size in MB."""
    total_size = 0
    model_short = model_name.split("/")[-1]
    
    for cache_dir in get_fastembed_cache_locations():
        if not os.path.exists(cache_dir):
            continue
        
        try:
            for folder in os.listdir(cache_dir):
                if model_short in folder or model_short.replace("-", "_") in folder:
                    folder_path = os.path.join(cache_dir, folder)
                    if os.path.isdir(folder_path):
                        for dirpath, dirnames, filenames in os.walk(folder_path):
                            for f in filenames:
                                fp = os.path.join(dirpath, f)
                                try:
                                    total_size += os.path.getsize(fp)
                                except Exception:
                                    pass
        except (PermissionError, OSError):
            continue
    
    return total_size / (1024 * 1024)


def delete_model(model_name):
    """Delete a cached model. Returns True if anything was deleted."""
    import shutil
    deleted = False

    model_short = model_name.split("/")[-1]

    for cache_dir in get_fastembed_cache_locations():
        if not os.path.exists(cache_dir):
            continue

        try:
            for folder in os.listdir(cache_dir):
                if model_short in folder or model_short.replace("-", "_") in folder:
                    folder_path = os.path.join(cache_dir, folder)
                    try:
                        shutil.rmtree(folder_path, ignore_errors=False)
                        deleted = True
                    except PermissionError:
                        shutil.rmtree(folder_path, ignore_errors=True)
                        deleted = True
        except (PermissionError, OSError):
            continue

    return deleted
