function InputField({
  label,
  type = "text",
  placeholder,
  value,
  onChange
}) {
  return (
    <div className="input-field">
      <label>{label}</label>

      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
}

export default InputField;