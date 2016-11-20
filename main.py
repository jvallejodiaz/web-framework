from werkzeug.wrappers import Request, Response

_request_stack = werkzeug.local.LocalStack()

@Request.application
def application(request):
    return Response('Hello World!')

def run(host, port, funct):
    from werkzeug.serving import run_simple
    run_simple(host, port, funct)

if __name__ == '__main__':
    run('localhost', 4000, application)
