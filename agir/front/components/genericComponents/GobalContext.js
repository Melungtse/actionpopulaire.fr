import React from "react";
import PropTypes from "prop-types";
import { ThemeProvider } from "styled-components";

import styles from "./style.scss";

/*
 * Objet proxy utilisé en test pour toujours renvoyer quelque chose
 */
const routes = new Proxy(
  {},
  {
    get(_target, name) {
      return `#${name}`;
    },
  }
);

const GobalContext = React.createContext({
  user: null,
  domain: "https://agir.lafranceinsoumise.fr",
  csrfToken: null,
  routes,
});

export const GlobalContextProvider = ({ children }) => {
  const globalContextScript = document.getElementById("globalContext");
  let globalContext = null;

  if (globalContextScript) {
    globalContext = JSON.parse(globalContextScript.textContent);
  }

  return (
    <GobalContext.Provider value={globalContext}>
      <ThemeProvider theme={styles}>{children}</ThemeProvider>
    </GobalContext.Provider>
  );
};
GlobalContextProvider.propTypes = {
  children: PropTypes.element,
};

export const useGlobalContext = () => React.useContext(GobalContext);

export const TestGlobalContextProvider = GobalContext.Provider;
