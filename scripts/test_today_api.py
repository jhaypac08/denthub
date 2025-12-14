"""Test script: login and call /api/patient/appointments/today/

Usage (PowerShell):
  python .\scripts\test_today_api.py --host http://192.168.1.18:8000 --username admin --password admin123

The script will:
 - open a requests.Session()
 - try to GET /admin/login/ to obtain CSRF token and POST credentials
 - if /admin/login/ is not available, try /api-auth/login/
 - finally GET the today endpoint and print status + JSON/text

Note: run this on the machine that can reach the LAN host. The endpoint requires authentication.
"""

import argparse
import sys
import requests
from urllib.parse import urljoin


def get_csrf_from_response_text(text):
    # Basic extraction of csrfmiddlewaretoken from HTML input
    import re
    m = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([0-9a-zA-Z-_.]+)['\"]", text)
    if m:
        return m.group(1)
    # fallback: search for cookie-based csrftoken header (requests will handle cookies)
    return None


def try_admin_login(session, base_url, username, password, timeout=10):
    login_path = '/admin/login/'
    login_url = urljoin(base_url, login_path)
    print(f'Trying admin login at {login_url}')
    try:
        r = session.get(login_url, timeout=timeout)
    except Exception as e:
        print('Error fetching admin login page:', e)
        return False

    if r.status_code not in (200, 302):
        print('Admin login page returned', r.status_code)
        return False

    csrf = None
    # requests will store cookies (including csrftoken) if set by server
    if 'csrftoken' in session.cookies:
        csrf = session.cookies.get('csrftoken')
    if not csrf:
        csrf = get_csrf_from_response_text(r.text)

    if not csrf:
        print('Could not determine CSRF token from admin login page; proceeding without explicit token')

    data = {
        'username': username,
        'password': password,
        'this_is_the_login_form': '1',
    }
    headers = {
        'Referer': login_url,
    }
    if csrf:
        data['csrfmiddlewaretoken'] = csrf
        # also set header usually set by browser
        headers['X-CSRFToken'] = csrf

    try:
        post = session.post(login_url, data=data, headers=headers, timeout=timeout, allow_redirects=True)
    except Exception as e:
        print('Error posting admin login:', e)
        return False

    # If login succeeded, Django admin redirects to /admin/ (302) and page contains "Log out"
    if post.status_code in (200, 302):
        # check for logout link in content
        if 'Log out' in post.text or 'Log out' in post.headers.get('Location', ''):
            print('Admin login appears successful')
            return True
        # If redirected to admin index
        if post.history and any(r.status_code == 302 for r in post.history):
            print('Admin login probably succeeded (redirected)')
            return True
        # sometimes admin returns 200 with dashboard HTML
        if 'Site administration' in post.text or 'Log out' in post.text:
            print('Admin login appears successful')
            return True

    print('Admin login did not appear successful (status', post.status_code, ')')
    return False


def try_api_auth_login(session, base_url, username, password, timeout=10):
    # Some projects expose DRF browsable login at /api-auth/login/
    login_path = '/api-auth/login/'
    login_url = urljoin(base_url, login_path)
    print(f'Trying API-auth login at {login_url}')
    try:
        r = session.get(login_url, timeout=timeout)
    except Exception as e:
        print('Error fetching api-auth login page:', e)
        return False

    csrf = session.cookies.get('csrftoken') or get_csrf_from_response_text(r.text)
    data = {'username': username, 'password': password}
    headers = {'Referer': login_url}
    if csrf:
        data['csrfmiddlewaretoken'] = csrf
        headers['X-CSRFToken'] = csrf

    try:
        post = session.post(login_url, data=data, headers=headers, timeout=timeout, allow_redirects=True)
    except Exception as e:
        print('Error posting api-auth login:', e)
        return False

    if post.status_code in (200, 302) and ('Log out' in post.text or post.history):
        print('api-auth login probably succeeded')
        return True

    print('api-auth login did not appear successful (status', post.status_code, ')')
    return False


def call_today_endpoint(session, base_url, timeout=10):
    path = '/api/patient/appointments/today/'
    url = urljoin(base_url, path)
    print('Requesting today endpoint:', url)
    try:
        r = session.get(url, timeout=timeout)
    except Exception as e:
        print('Error requesting today endpoint:', e)
        return
    print('STATUS', r.status_code)
    print('HEADERS:')
    for k, v in r.headers.items():
        print(' ', k, ':', v)
    try:
        data = r.json()
        print('\nJSON RESPONSE:')
        import json as _json
        print(_json.dumps(data, indent=2, ensure_ascii=False))
    except Exception:
        print('\nTEXT RESPONSE:')
        print(r.text[:20000])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='http://127.0.0.1:8000', help='Base host (include http://)')
    p.add_argument('--username', default='admin')
    p.add_argument('--password', default='admin123')
    p.add_argument('--timeout', type=int, default=10)
    args = p.parse_args()

    sess = requests.Session()
    sess.headers.update({'User-Agent': 'DenthubTestClient/1.0'})

    base = args.host.rstrip('/') + '/'

    # Try admin login first
    ok = try_admin_login(sess, base, args.username, args.password, timeout=args.timeout)
    if not ok:
        ok = try_api_auth_login(sess, base, args.username, args.password, timeout=args.timeout)

    if not ok:
        print('Login attempts failed. You may need to provide different credentials or enable an API login endpoint.')
        print('Proceeding to call the today endpoint without an authenticated session (may return 401/403 or empty).')

    call_today_endpoint(sess, base, timeout=args.timeout)
