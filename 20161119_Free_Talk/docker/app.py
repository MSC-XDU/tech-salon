# -*- coding:utf-8 -*-
__author__ = 'calculusma'

from flask import Flask,request,render_template,Response
from docker import Client
import time,datetime

def init():
    c = Client(base_url="unix://var/run/docker.sock")
    # cid = c.create_container(
    #             image="python:2.7.12-slim",
    #             volumes='/codebase',
    #             host_config=c.create_host_config(binds={
    #                 os.getcwd()+'/tmp':{
    #                     "bind":"/codebase",
    #                     "mode":"ro"
    #                     }
    #                 }
    #             ),
    #             command="python /codebase/test.py"
    #         )["Id"]
    cid = "478dc814cb51"
    return c,cid

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        code = request.form.get("code")
        t = int(time.time())
        with open("tmp/test.py", "w+") as f:
            f.write(code.encode('utf-8'))
        c.start(cid)
        result = c.logs(cid,
                        since=t,
                        # stream=True,
                        # timestamps=True
        )
        return Response(result,mimetype="text")
    return render_template("index.html")


@app.route("/test")
def test():
#    def g():
#        for i in range(1000):
#            time.sleep(0.1)
#            yield str(i)+" "
#    sg = g()
#    return Response(sg, mimetype="text/event-stream")
    return render_template("test.html")

if __name__ == "__main__":
    c, cid = init()
    app.run(port=5000, debug=True)
