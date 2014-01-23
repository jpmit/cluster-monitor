from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import paramiko
import json

class JobDataManager(object):
    """
    Handles ssh commands and stores data that can be retrieved by the
    HTTP request handler.
    """

    MACHINE_NAME = 'eugenegm'

    def __init__(self):
    
        self.ssh = paramiko.SSHClient()

        # if the machine we are connecting to isn't in 'known hosts',
        # add it automatically rather than raising an exception.
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # we keep a persistent connection to the machine, and poll it
        # for information when required.
        self.ssh.connect(MACHINE_NAME)

    def get_job_info(self):
        """Return data for all running jobs."""

        # get list of all running jobs
        ssh_in, ssh_out, ssh_err = self.ssh.exec_command("qstat | grep '   r'")

        # make alljobs a list
        alljobs = ssh_out.read().split('\n')
        alljobs = [j.strip() for j in alljobs if j != '']
        
        # get job ids for all running jobs
        ids = [j.split()[0] for j in alljobs]
        ids = list(set(ids))
        ids.sort()

        # get detailed job information for all the running jobs
        # (filter for cwd for now)
        cmd = "qstat -j {} | grep cwd".format(','.join(ids))
        ssh_in, ssh_out, ssh_err = self.ssh.exec_command(cmd)        
        dirs = ssh_out.read().split('\n')
        dirs = [d.split()[1] for d in dirs if d != '']
        dirs.sort()
        
        # this JSON data is returned to the browser
        data = {'alljobs': alljobs, 'dirs': dirs}
        return json.dumps(data)

class MyHTTPServer(HTTPServer):
    def __init__(self, address, handler):
        HTTPServer.__init__(self, address, handler)
        self.setup_dmanager(handler)

    def setup_dmanager(self, handler):
        """Add the data manager to the request handler."""

        # the handler accesses information stored by the data manager
        # when it receives GET requests (via AJAX).
        handler.dmanager = JobDataManager()
        
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    ROOTDIR = '/home/ph/stf/jm0037/awork/python/server/files/'
    
    def do_GET(self):
        """Handle get request."""

        if self.path.endswith('monitor'):
            # AJAX calls go here
            data = self.dmanager.get_job_info()
            ctype = 'application-json'
        else:
            # 'normal' page
            try:
                f = open(self.ROOTDIR + self.path)
            except IOError:
                self.send_error(404, 'file not found')
            data = f.read()
            f.close()
            ctype = 'text-html'

        # send code 200 response
        self.send_response(200)

        # send header first
        self.send_header('Content-type', ctype)
        self.end_headers()

        # send content to client
        self.wfile.write(data)

def run_server():
    print('http server is starting...')

    # use port 8080 since OS wont allow < 1024 without being root
    server_address = ('127.0.0.1', 8080)
    httpd = MyHTTPServer(server_address, MyHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run_server()
