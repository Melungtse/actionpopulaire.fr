import style from "@agir/front/genericComponents/_variables.scss";
import Card from "./Card";
import React, { useCallback, useRef, useState } from "react";
import Button from "./Button";
import { Column, Row } from "./grid";
import facebookLogo from "./logos/facebook.svg";
import twitterLogo from "./logos/twitter.svg";
import telegramLogo from "./logos/telegram.svg";
import whatsappLogo from "./logos/whatsapp.svg";

let logoSpacing = { margin: "0 8px" };

const ShareCard = () => {
  let [copied, setCopied] = useState(false);
  let copyUrl = useCallback(() => {
    inputEl.current.select();
    document.execCommand("copy");
    setCopied(true);
  }, []);

  const inputEl = useRef(null);
  let encodedLocation = encodeURIComponent(window.location.href);
  return (
    <Card style={{ padding: "1.5rem" }}>
      <Row gutter={2} style={{ marginBottom: "1rem" }}>
        <Column grow collapse={false}>
          <b>Partager</b>
        </Column>
        <Column collapse={false}>
          <a href={`https://wa.me/?text=${encodedLocation}`}>
            <img src={whatsappLogo} style={logoSpacing} alt="Whatsapp" />
          </a>
          <a href={`https://t.me/share/url?url=${encodedLocation}`}>
            <img src={telegramLogo} style={logoSpacing} alt="Telegram" />
          </a>
          <a
            href={`https://www.facebook.com/sharer/sharer.php?u=${encodedLocation}`}
          >
            <img src={facebookLogo} style={logoSpacing} alt="Facebook" />
          </a>
          <a href={`https://twitter.com/intent/tweet?text=${encodedLocation}`}>
            <img
              src={twitterLogo}
              style={{ ...logoSpacing, marginRight: 0 }}
              alt="Twitter"
            />
          </a>
        </Column>
      </Row>

      <Row gutter={4}>
        <Column grow collapse={false}>
          {" "}
          <input
            type="text"
            value={window.location.href}
            style={{
              width: "100%",
              height: "32px",
              border: `1px solid ${style.black100}`,
              borderRadius: "8px",
              padding: "8px",
            }}
            readOnly
            ref={inputEl}
            onClick={copyUrl}
          />
        </Column>
        <Column collapse={false}>
          <Button small icon={copied ? "check" : "copy"} onClick={copyUrl}>
            Copier le lien
          </Button>
        </Column>
      </Row>
    </Card>
  );
};
export default ShareCard;
