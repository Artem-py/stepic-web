def application(environ, start_response):
    query = environ['QUERY_STRING'].split('&')
    data = '\n'.join(query).encode('UTF-8')
    
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain')
    ]
    start_response(status, response_headers)
    
    return data
