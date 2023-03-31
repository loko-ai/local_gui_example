<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>Local GUI</h1><br></html>

**Local GUI** example shows how to integrate your extensions with custom GUIs.

From the **Projects**'s tab, click on **Import from git** and copy and paste the URL of the current page 
(i.e. https://github.com/loko-ai/local_gui_example):
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229048981-e03d7b6f-6ef4-4064-8c0e-75052497744a.png" width="60%" /></p>

Once the project is downloaded, click and open it.  In order to start the project remember to press the **play** button on the right of the project's name.
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229137120-81ff7b90-9f21-452d-8e79-694d6831d63b.png" width="80%" /></p>

You can click on **click me gui** to open the example GUI.

<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229138244-d529717a-e7fa-4bb9-9c2a-1af6432473a4.png" width="80%" /></p>

Let's now see how to custom the extension (See more here <a href="https://github.com/loko-ai/loko/wiki/Custom-extensions">Custom extensions</a>). 

Click right on the project's name on *Open in editor* (configure your editor using the Loko's settings first):
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229139890-2abc4dc6-b0d3-42ca-bfc8-3ecd44203ca3.png" width="80%" /></p>

Otherwise, you can open your project directly on the Loko's directory (i.e. `~/loko/projects/local_gui_example`).

### Frontend

In `/local_gui_example/frontend/src/App.jsx` you'll find the simple button shown in the GUI:

```
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import { Box, Button, Flex, Input } from "@chakra-ui/react";
import axios from "axios";
import urljoin from "url-join";
const baseURL = import.meta.env.VITE_BASE_URL || "/";

console.log(baseURL);
function App() {
  const [content, setContent] = useState();

  return (
    <Flex direction="column">
      <Button
        onClick={async (e) => {
          const resp = await axios.get(urljoin(baseURL, "content"));
          setContent(resp.data);
        }}
      >
        Click me please
      </Button>
      <Box>{content}</Box>
    </Flex>
  );
}

export default App;
```

When you click on **Click me please**, it requests the service `/content` on *baseURL* (i.e. `/routes/local_gui_example`).

### Services

In `/local_gui_example/services/services.py` you'll find the *content* service:

```
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask("prova_gui", static_url_path="/web", static_folder="/frontend/dist")

@app.get("/content")
def content():
    return f"Hello {time.time()}"


CORS(app)

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)


```

### Config

Now we have to link the GUI to the extension in `local_gui_example/config.json`: 

```
{
  "main": {
    "gui": {
      "name": "click me gui"
    }
  }
}
```

Here we can set the GUI's name, which in this case is **click me gui**.

### Dockerfile

Once you prepared your frontend, services and config, you have to configure the Dockerfile of your 
container:

```
FROM node:16.15.0 AS builder
ADD ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN yarn install
ADD ./frontend /frontend
RUN yarn build --base="/routes/local_gui_example/web/"

FROM python:3.10-slim
EXPOSE 8080
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
COPY --from=builder /frontend/dist /frontend/dist
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
CMD python services.py
```

When you **stop** your project and click again on the **play** button, Loko builds a new image, and you're ready to use 
your extension. 
