import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import Button from "@agir/front/genericComponents/Button";

import style from "@agir/front/genericComponents/_variables.scss";

import imgStep1 from "./images/step_1.png";
import imgStep2 from "./images/step_2.png";
import imgStep3 from "./images/step_3.png";
import imgStep4 from "./images/step_4.png";

const StyledStep = styled.div`
  text-align: center;
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
  justify-content: center;
  max-width: 600px;
  min-height: 441px;
  padding: 36px 40px;
  margin: 60px auto 0;
  box-shadow: ${style.elaborateShadow};
  border-radius: 8px;
  background-color: ${style.white};

  @media (max-width: ${style.collapse}px) {
    margin: 20px auto 0;
    min-height: 510px;
    max-width: calc(100% - 40px);
    padding: 36px 25px;
  }

  img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: ${({ imgHeight }) => imgHeight || 126}px;
    margin-bottom: 25px;
    margin-top: 0;

    @media (max-width: ${style.collapse}px) {
      margin-bottom: 16px;
      background-position: bottom center;
    }
  }

  h2 {
    font-size: 20px;
    line-height: 1.5;
    margin-bottom: 16px;
    margin-top: 0;

    em {
      color: ${style.primary500};
    }

    a {
      color: inherit;
      text-decoration: underline;
    }
  }

  p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 25px;
  }
`;

export const Step = (props) => {
  const { img, imgHeight, title, body, onClick, hasNext = false } = props;
  return (
    <StyledStep imgHeight={imgHeight}>
      {img ? <img src={img} /> : null}
      <h2>{title}</h2>
      {body}
      <Button color="primary" onClick={onClick}>
        {hasNext ? "Suivant" : "Accéder au site"}
      </Button>
    </StyledStep>
  );
};
Step.propTypes = {
  img: PropTypes.string,
  imgHeight: PropTypes.number,
  title: PropTypes.node.isRequired,
  body: PropTypes.node.isRequired,
  onClick: PropTypes.func.isRequired,
  hasNext: PropTypes.bool,
};

export const steps = [
  {
    img: imgStep1,
    imgHeight: 126,
    title: (
      <>
        La plate-forme d'action de la France insoumise devient{" "}
        <em>Action Populaire</em>
      </>
    ),
    body: (
      <p>
        Pas de panique ! Vous êtes au bon endroit et on va tout vous expliquer.
        C’est très simple.
      </p>
    ),
  },
  {
    img: imgStep2,
    imgHeight: 90,
    title: (
      <>
        Retrouvez les actualités de la FI sur{" "}
        <a href="httsp://lafranceinsomuise.fr">lafranceinsoumise.fr</a>
      </>
    ),
    body: (
      <p>
        Ce site est maintenant consacré à l’organisation des militants et des
        groupes d’action FI.
      </p>
    ),
  },
  {
    img: imgStep3,
    imgHeight: 110,
    title: <>Vos groupes, vos événement et vos notifications au même endroit</>,
    body: (
      <p>
        Le menu vous permet d’accéder d’un coup d’oeil à toute votre vie
        militante. Pratique !
      </p>
    ),
  },
  {
    img: imgStep4,
    title: <>Un espace pour toutes vos tâches militantes à traiter 👍</>,
    body: (
      <p>
        En cas de problème, ou bien lorsque des nouveaux membre rejoignent votre
        groupe, recevez l’information en priorité.
      </p>
    ),
  },
  {
    img: null,
    imgHeight: 120,
    title: <>Et ce n'est pas fini !</>,
    body: (
      <p>
        Nos équipes vont travailler avec vous pour améliorer la plate-forme.
        Nous vous présenterons bientôt de nouvelles fonctionnalités pour vous
        simplifier la vie.
      </p>
    ),
  },
];

const Steps = (props) => {
  const { onClose } = props;
  const [activeStep, setActiveStep] = React.useState(0);
  const hasNext = React.useMemo(() => !!steps[activeStep + 1], [activeStep]);
  const handleNext = React.useCallback(() => {
    if (hasNext) {
      return setActiveStep((state) => state + 1);
    }
    return onClose();
  }, [onClose, hasNext]);

  return <Step {...steps[activeStep]} hasNext={hasNext} onClick={handleNext} />;
};

Steps.propTypes = {
  onClose: PropTypes.func.isRequired,
};

export default Steps;
