from dash_bio.utils import PdbParser, create_mol3d_style
import hashlib
from pathlib import Path
import pickle


cache_dir = Path('private-data/cache')
cache_dir.mkdir(parents=True, exist_ok=True)


def _hash_file(path: Path):
    sha2 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha2.update(chunk)
    return sha2.hexdigest()


def load_pdb(pdb_path: Path, verbose=False):
    # compute md5sum of file
    sha2 = _hash_file(pdb_path)
    cached_path = cache_dir.joinpath(f'{sha2}.pkl')
    if cached_path.exists():
        if verbose:
            print(f'Loading cached {cached_path}', flush=True)

        with open(cached_path, 'rb') as f:
            return pickle.load(f)

    if verbose:
        print(f'Parsing {pdb_path}', flush=True)

    parser = PdbParser(pdb_path.as_posix())
    data = parser.mol3d_data()
    styles = create_mol3d_style( data['atoms'], visualization_type='cartoon')
    with open(cached_path, 'wb') as f:
        pickle.dump((data, styles), f)

    return data, styles