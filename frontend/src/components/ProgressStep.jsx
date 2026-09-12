function ProgressStep({ currentStep }) {
  const steps = ["Profile", "Results", "Scheme Details", "Partners"];

  return (
    <div className="progress-container">
      <div className="progress-steps">
        {steps.map((step, index) => {
          const stepNumber = index + 1;
          const state = stepNumber < currentStep ? "completed" : stepNumber === currentStep ? "active" : "";
          return (
            <div key={step} className={`progress-step ${state}`}>
              <div className="progress-circle">{stepNumber < currentStep ? "✓" : stepNumber}</div>
              <span>{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ProgressStep;
