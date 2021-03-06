(async function () {
  const [
    { default: React },
    { renderReactComponent },
    { default: IBANField },
    { default: onDOMReady },
  ] = await Promise.all([
    import("react"),
    import("@agir/lib/utils/react"),
    import("./IBAN-field"),
    import("@agir/lib/utils/onDOMReady"),
  ]);

  const renderIBANField = () => {
    const fields = document.querySelectorAll(
      'input[data-component="IBANField"]'
    );

    for (let field of fields) {
      const renderingNode = document.createElement("div");
      const parent = field.parentNode;
      renderReactComponent(
        <IBANField
          name={field.name}
          id={field.id}
          allowedCountries={
            field.dataset.allowedCountries
              ? field.dataset.allowedCountries.split(",")
              : null
          }
          placeholder={field.placeholder}
          initial={field.value}
        />,
        renderingNode
      );
      parent.insertBefore(renderingNode, field);
      parent.removeChild(field);
    }
  };

  onDOMReady(renderIBANField);
})();
