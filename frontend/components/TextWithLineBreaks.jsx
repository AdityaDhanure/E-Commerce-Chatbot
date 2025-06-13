import React from 'react';

// This component takes a text prop, removes Markdown bold syntax, and displays the text with line breaks
const removeMarkdownBold = (text) => {
  return text.replace(/\*\*(.*?)\*\*/g, '$1');
};

const TextWithLineBreaks = ({ text }) => {
  if (!text) return null;

  const cleanedText = removeMarkdownBold(text);
  const lines = cleanedText.split('\n');

  return (
    <>
      {lines.map((item, key) => (
        <React.Fragment key={key}>
          {item}
          {/* Add a <br /> for each newline, except after the very last line */}
          {key < lines.length - 1 && <br />}
        </React.Fragment>
      ))}
    </>
  );
};

export default TextWithLineBreaks;