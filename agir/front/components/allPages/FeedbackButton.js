import PropTypes from "prop-types";
import React, { useCallback, useEffect, useState } from "react";
import { useTransition, animated } from "react-spring";
import styled from "styled-components";

import style from "@agir/front/genericComponents/_variables.scss";

import { useGlobalContext } from "@agir/front/genericComponents/GlobalContext";

import background from "./feedback-form-button.svg";
import closeButton from "./close-btn.svg";

const slideInTransition = {
  from: { opacity: 0, marginBottom: "-3rem" },
  enter: { opacity: 1, marginBottom: "0" },
  leave: { opacity: 0, marginBottom: "-3rem" },
};

const fadeInTransition = {
  from: { opacity: 0 },
  enter: { opacity: 1 },
  leave: { opacity: 0 },
  delay: 200,
};

const Tooltip = styled(animated.p)`
  position: absolute;
  top: -10px;
  right: 0;
  transform: translate(-26px, -100%);
  right: 0;
  width: 175px;
  background-color: ${style.black1000};
  color: white;
  padding: 1rem;
  display: flex;
  flex-flow: column nowrap;
  font-size: 13px;
  line-height: 1.3;

  strong {
    font-size: 14px;
  }

  button {
    position: absolute;
    top: 0;
    right: 0;
    transform: translate(50%, -50%);
    width: 24px;
    height: 24px;
    background-color: transparent;
    border: none;
    background-image: url(${closeButton});
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    cursor: pointer;
  }

  :after {
    content: "";
    position: absolute;
    top: 100%;
    right: 0;
    margin-left: -4px;
    border-width: 4px;
    border-style: solid;
    border-color: black black transparent transparent;
  }
`;

const Button = styled.a`
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 100%;
  background-color: transparent;
  background-image: url(${background});
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
`;

const Wrapper = styled(animated.div)`
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  width: 53px;
  height: 53px;
  z-index: ${style.zindexFeedbackButton};

  @media (max-width: ${style.collapse}px) {
    bottom: 75px;
  }
`;

export const FeedbackButton = (props) => {
  const { isActive, shouldPushTooltip, href } = props;

  const [hasTooltip, setHasTooltip] = useState(false);

  const hideTooltip = useCallback(() => {
    setHasTooltip(false);
  }, []);

  const showTooltip = useCallback(() => {
    setHasTooltip(true);
  }, []);

  const pushTooltip = useCallback(() => {
    shouldPushTooltip && showTooltip();
  }, [shouldPushTooltip, showTooltip]);

  const tooltipTransition = useTransition(hasTooltip, null, fadeInTransition);
  const wrapperTransition = useTransition(isActive, null, {
    ...slideInTransition,
    onRest: pushTooltip,
  });

  return wrapperTransition.map(({ item, key, props }) =>
    item ? (
      <Wrapper key={key} style={props}>
        {tooltipTransition.map(({ item, key, props }) =>
          item ? (
            <Tooltip key={key} style={props}>
              <strong>Aidez-nous !</strong>
              <span>Donnez votre avis sur le nouveau site →</span>
              {shouldPushTooltip ? (
                <button aria-label="Cacher" onClick={hideTooltip} />
              ) : null}
            </Tooltip>
          ) : null
        )}
        <Button
          href={href}
          aria-label="Je donne mon avis"
          onMouseOver={shouldPushTooltip ? undefined : showTooltip}
          onMouseLeave={shouldPushTooltip ? undefined : hideTooltip}
        />
      </Wrapper>
    ) : null
  );
};
FeedbackButton.propTypes = {
  isActive: PropTypes.bool,
  shouldPushTooltip: PropTypes.bool,
  href: PropTypes.string.isRequired,
};
const ConnectedFeedbackButton = (props) => {
  const { routes } = useGlobalContext();
  const href = routes && routes.feedbackForm;

  const [isActive, setIsActive] = useState(false);
  const [shouldPushTooltip, setShouldPushTooltip] = useState(false);

  useEffect(() => {
    if (!window.localStorage) {
      return;
    }
    let visitCount = window.localStorage.getItem("AP_vcount");
    visitCount = !isNaN(parseInt(visitCount)) ? parseInt(visitCount) : 0;
    visitCount += 1;
    visitCount % 20 === 3 && setShouldPushTooltip(true);
    setIsActive(true);
    window.localStorage.setItem("AP_vcount", visitCount);
  }, []);

  return (
    <FeedbackButton
      {...props}
      href={href}
      isActive={isActive}
      shouldPushTooltip={shouldPushTooltip}
    />
  );
};
export default ConnectedFeedbackButton;
