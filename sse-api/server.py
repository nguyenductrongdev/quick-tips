from flask import Flask, Response, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html>
            <head>
                <title>Flask SSE</title>
            </head>
            <body>
                <h1>Server-Sent Events with Flask</h1>
                <div id="events"></div>
                <script type="text/javascript">
                    var eventSource = new EventSource("/stream");

                    eventSource.onmessage = function(event) {
                        console.log(event);
                        var newElement = document.createElement("div");
                        newElement.innerHTML = "New message: " + event.data;
                        document.getElementById("events").appendChild(newElement);
                    };

                    eventSource.addEventListener('close', function(event) {
                        eventSource.close();
                        var newElement = document.createElement("div");
                        newElement.innerHTML = "Connection closed.";
                        document.getElementById("events").appendChild(newElement);
                    });
                </script>
            </body>
        </html>
    ''')

@app.route('/stream')
def stream():
    def generate():
        import time
        for i in range(1, 11):
            yield f"data: {i}\n\n"
            time.sleep(0.2)
        yield "event: close\ndata: Connection closed\n\n"  # Send close event
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
