'use client';

import { useState, useCallback } from 'react';

export interface ValidationRule {
  validate: (value: any) => boolean;
  message: string;
}

export interface FormErrors {
  [key: string]: string | undefined;
}

export interface ValidationRules {
  [key: string]: ValidationRule[];
}

export function useFormValidation(initialValues: Record<string, any>, rules: ValidationRules) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = useCallback(
    (fieldName: string, value: any): string | undefined => {
      if (!rules[fieldName]) {
        return undefined;
      }

      for (const rule of rules[fieldName]) {
        if (!rule.validate(value)) {
          return rule.message;
        }
      }
      return undefined;
    },
    [rules]
  );

  const handleChange = useCallback(
    (fieldName: string, value: any) => {
      setValues((prev) => ({
        ...prev,
        [fieldName]: value,
      }));

      if (touched[fieldName]) {
        const error = validateField(fieldName, value);
        setErrors((prev) => ({
          ...prev,
          [fieldName]: error,
        }));
      }
    },
    [touched, validateField]
  );

  const handleBlur = useCallback((fieldName: string) => {
    setTouched((prev) => ({
      ...prev,
      [fieldName]: true,
    }));

    const error = validateField(fieldName, values[fieldName]);
    setErrors((prev) => ({
      ...prev,
      [fieldName]: error,
    }));
  }, [values, validateField]);

  const validateAll = useCallback((): boolean => {
    const newErrors: FormErrors = {};
    let isValid = true;

    Object.keys(rules).forEach((fieldName) => {
      const error = validateField(fieldName, values[fieldName]);
      if (error) {
        newErrors[fieldName] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    setTouched(
      Object.keys(rules).reduce((acc, key) => {
        acc[key] = true;
        return acc;
      }, {} as Record<string, boolean>)
    );

    return isValid;
  }, [rules, values, validateField]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateAll,
    reset,
    setValues,
  };
}
