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
