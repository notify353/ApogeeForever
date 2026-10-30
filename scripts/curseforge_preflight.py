"""Read-only authenticated client-version lookup. Never uploads or prints credentials."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

URL = 'https://wow.curseforge.com/api/game/versions'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Authenticated redirect refused')

def select_version(rows, target="forever"):
    from release_manifest import TARGETS
    if target not in TARGETS: raise ValueError("Unknown client target")
    expected = TARGETS[target]
    if not isinstance(rows, list):
        raise ValueError('Unexpected version response')
    matches = [row for row in rows if isinstance(row, dict)
               and row.get('name') == expected['name'] and row.get('gameVersionTypeID') == expected['gameVersionTypeID']]
    if len(matches) != 1:
        raise ValueError('Exactly one '+target+' '+expected['name']+' upload version is required; no fallback')
    row = matches[0]
    if type(row.get('id')) is not int or row['id'] <= 0 or row['id'] == expected['gameVersionTypeID']:
        raise ValueError('Invalid upload version ID')
    return {key: row[key] for key in ('id', 'name', 'gameVersionTypeID')}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=('forever','classic-era'), default='forever')
    parser.add_argument('--version')
    args=parser.parse_args()
    if args.version:
        import release_manifest as r
        args.target=r.load(args.version)[0]['target']
    token = os.environ.get('CF_API_KEY')
    if not token:
        sys.exit('CurseForge credential is unavailable')
    request = urllib.request.Request(URL, headers={'X-Api-Token': token, 'Accept': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
            result = select_version(json.load(response), args.target)
    except urllib.error.HTTPError as error:
        sys.exit('CurseForge preflight HTTP status ' + str(error.code))
    except (ValueError, OSError):
        sys.exit('CurseForge exact '+args.target+' version lookup failed; no upload attempted')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
