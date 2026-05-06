'use client';

interface FormErrorProps {
  message?: string;
  className?: string;
}

export function FormError({ message, className = '' }: FormErrorProps) {
  if (!message) return null;

  return (
    <div className={`text-sm text-red-600 mt-1 flex items-start gap-1 ${className}`}>
      <span className="text-red-500 mt-0.5">⚠</span>
      <span>{message}</span>
    </div>
  );
}

interface FormFieldProps {
  label: string;
  name: string;
  type?: string;
  value: any;
  onChange: (name: string, value: any) => void;
  onBlur: (name: string) => void;
  error?: string;
  touched?: boolean;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export function FormField({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  touched,
  placeholder,
  required,
  disabled,
  className = '',
  children,
}: FormFieldProps) {
  const hasError = touched && error;

  if (children) {
    return (
      <div className={`flex flex-col gap-2 ${className}`}>
        <label htmlFor={name} className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
        <div className={hasError ? 'border-b-2 border-red-500' : ''}>
          {children}
        </div>
        {hasError && <FormError message={error} />}
      </div>
    );
  }

  return (
    <div className={`flex flex-col gap-2 ${className}`}>
      <label htmlFor={name} className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(name, e.target.value)}
        onBlur={() => onBlur(name)}
        placeholder={placeholder}
        disabled={disabled}
        className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 transition-colors ${
          hasError
            ? 'border-red-500 focus:ring-red-500 bg-red-50'
            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
        } ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
      />
      {hasError && <FormError message={error} />}
    </div>
  );
}
