function Dropdown({ label, value, onChange, options }) {
  return (
    <div className="dropdown-field">
      <label>{label}</label>

      <select value={value} onChange={onChange}>
        <option value="">Select an option</option>

        {options.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}

export default Dropdown;