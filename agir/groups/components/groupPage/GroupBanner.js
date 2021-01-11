import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";

import style from "@agir/front/genericComponents/_variables.scss";

import StaticMap from "@agir/carte/common/StaticMap";

const StyledMap = styled.div``;
const StyledBanner = styled.div`
  display: flex;
  flex-flow: row-reverse nowrap;
  background-color: ${style.secondary500};
  max-width: 1090px;
  margin: 0 auto;

  @media (max-width: ${style.collapse}px) {
    max-width: 100%;
    flex-flow: column nowrap;
    background-color: transparent;
  }

  header {
    flex: 1 1 auto;
    padding: 2.25rem 2.25rem;

    @media (max-width: ${style.collapse}px) {
      padding: 1.5rem;
    }
  }

  h2,
  h4 {
    margin: 0;
    &::first-letter {
      text-transform: uppercase;
    }
  }

  h2 {
    font-weight: 700;
    font-size: 1.75rem;
    line-height: 1.419;
    margin-bottom: 0.5rem;

    @media (max-width: ${style.collapse}px) {
      font-size: 1.25rem;
      line-height: 1.519;
    }
  }

  h4 {
    font-size: 1rem;
    font-weight: 500;
    line-height: 1.5;

    @media (max-width: ${style.collapse}px) {
      font-size: 0.875rem;
    }
  }

  ${StyledMap} {
    flex: 0 0 424px;
    clip-path: polygon(100% 0%, 100% 100%, 0% 100%, 11% 0%);

    @media (max-width: ${style.collapse}px) {
      clip-path: none;
      width: 100%;
      flex-basis: 155px;
    }
  }
`;

const GroupBanner = (props) => {
  const { name, type, location } = props;

  const subtitle = React.useMemo(() => {
    const { city, zip } = location || {};
    if (!zip) {
      return type;
    }
    if (!city) {
      return `${type} (${zip})`;
    }
    return `${type} à ${city} (${zip})`;
  }, [type, location]);

  return (
    <StyledBanner>
      {Array.isArray(location.coordinates) ? (
        <StyledMap>
          <StaticMap center={location.coordinates} />
        </StyledMap>
      ) : null}
      <header>
        <h2>{name}</h2>
        <h4>{subtitle}</h4>
      </header>
    </StyledBanner>
  );
};
GroupBanner.propTypes = {
  name: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  location: PropTypes.shape({
    city: PropTypes.string,
    zip: PropTypes.string,
    coordinates: PropTypes.arrayOf(PropTypes.number),
  }).isRequired,
};
export default GroupBanner;
