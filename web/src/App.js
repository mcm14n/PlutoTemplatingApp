import React from "react";
import styled from "styled-components";
import "./App.css";

import { renderTemplate } from "./utils/_api";

const RenderTemplateContainer = styled.div`
  & h5 {
    margin-bottom: 1em;
  }
`;

function App() {
  const [template, setTemplate] = React.useState("");
  const [renderedTemplate, setRenderedTemplate] = React.useState("");

  // event handler for user input
  const captureTemplate = (evt) => {
    const value = evt?.target?.value;
    setTemplate(value);
  };

  // callback to process template
  const processTemplate = () => {
    setRenderedTemplate("");
    renderTemplate(template)
      .then(({ data }) => {
        setRenderedTemplate(data.template);
      })
      .catch((err) => {
        console.log(err);
        setRenderedTemplate(err.response.data.description);
      });
  };

  return (
    <div className="App">
      <header>
        <h1>Pluto Templating System</h1>
      </header>
      <br />
      <h5 className="template-header">Please Enter Template Below:</h5>
      <br />
      <textarea
        className="template-text"
        rows={25}
        cols={100}
        onChange={captureTemplate}
        value={template}
      ></textarea>
      <br />
      <button
        className="process-button button is-primary is-large"
        onClick={processTemplate}
      >
        Process
      </button>
      {renderedTemplate && (
        <RenderTemplateContainer>
          <h5>Rendered Template</h5>
          <textarea className="template-text" rows={25} cols={100}>
            {renderedTemplate}
          </textarea>
        </RenderTemplateContainer>
      )}
    </div>
  );
}

export default App;
