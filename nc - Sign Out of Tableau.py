def signout():
    signout_url = "https://{server}/api/{version}/auth/signout".format(
        server=server_name, version=version)
    req = s.post(signout_url, data=b'', headers=headers)
    req.raise_for_status()
    print('singout successful')
signout()
