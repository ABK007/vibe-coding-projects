"use client";

import { useState } from "react";
import styles from "./Calculator.module.css";

export default function Calculator() {
  const [display, setDisplay] = useState("0");
  const [previousValue, setPreviousValue] = useState<string | null>(null);
  const [operation, setOperation] = useState<string | null>(null);
  const [shouldResetDisplay, setShouldResetDisplay] = useState(false);

  const handleNumberClick = (num: string) => {
    if (shouldResetDisplay) {
      setDisplay(num);
      setShouldResetDisplay(false);
    } else {
      setDisplay(display === "0" ? num : display + num);
    }
  };

  const handleOperationClick = (op: string) => {
    if (previousValue !== null && operation !== null && !shouldResetDisplay) {
      const result = calculate(
        parseFloat(previousValue),
        parseFloat(display),
        operation
      );
      setDisplay(result.toString());
      setPreviousValue(result.toString());
    } else {
      setPreviousValue(display);
    }
    setOperation(op);
    setShouldResetDisplay(true);
  };

  const handleEquals = () => {
    if (previousValue !== null && operation !== null) {
      const result = calculate(
        parseFloat(previousValue),
        parseFloat(display),
        operation
      );
      setDisplay(result.toString());
      setPreviousValue(null);
      setOperation(null);
      setShouldResetDisplay(true);
    }
  };

  const calculate = (a: number, b: number, op: string): number => {
    switch (op) {
      case "+":
        return a + b;
      case "-":
        return a - b;
      case "×":
        return a * b;
      case "÷":
        return b !== 0 ? a / b : 0;
      default:
        return b;
    }
  };

  const handleClear = () => {
    setDisplay("0");
    setPreviousValue(null);
    setOperation(null);
    setShouldResetDisplay(false);
  };

  const handleDecimal = () => {
    if (shouldResetDisplay) {
      setDisplay("0.");
      setShouldResetDisplay(false);
    } else if (!display.includes(".")) {
      setDisplay(display + ".");
    }
  };

  const handleBackspace = () => {
    if (display.length > 1) {
      setDisplay(display.slice(0, -1));
    } else {
      setDisplay("0");
    }
  };

  const handlePercentage = () => {
    const value = parseFloat(display);
    setDisplay((value / 100).toString());
  };

  const handleToggleSign = () => {
    const value = parseFloat(display);
    setDisplay((-value).toString());
  };

  return (
    <div className={styles.calculator}>
      <div className={styles.display}>
        <div className={styles.previousOperation}>
          {previousValue !== null && operation !== null
            ? `${previousValue} ${operation}`
            : "\u00A0"}
        </div>
        <div className={styles.currentValue}>{display}</div>
      </div>
      <div className={styles.buttons}>
        <button
          className={`${styles.button} ${styles.function}`}
          onClick={handleClear}
        >
          AC
        </button>
        <button
          className={`${styles.button} ${styles.function}`}
          onClick={handleToggleSign}
        >
          +/-
        </button>
        <button
          className={`${styles.button} ${styles.function}`}
          onClick={handlePercentage}
        >
          %
        </button>
        <button
          className={`${styles.button} ${styles.operator}`}
          onClick={() => handleOperationClick("÷")}
        >
          ÷
        </button>

        <button
          className={styles.button}
          onClick={() => handleNumberClick("7")}
        >
          7
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("8")}
        >
          8
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("9")}
        >
          9
        </button>
        <button
          className={`${styles.button} ${styles.operator}`}
          onClick={() => handleOperationClick("×")}
        >
          ×
        </button>

        <button
          className={styles.button}
          onClick={() => handleNumberClick("4")}
        >
          4
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("5")}
        >
          5
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("6")}
        >
          6
        </button>
        <button
          className={`${styles.button} ${styles.operator}`}
          onClick={() => handleOperationClick("-")}
        >
          -
        </button>

        <button
          className={styles.button}
          onClick={() => handleNumberClick("1")}
        >
          1
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("2")}
        >
          2
        </button>
        <button
          className={styles.button}
          onClick={() => handleNumberClick("3")}
        >
          3
        </button>
        <button
          className={`${styles.button} ${styles.operator}`}
          onClick={() => handleOperationClick("+")}
        >
          +
        </button>

        <button
          className={`${styles.button} ${styles.zero}`}
          onClick={() => handleNumberClick("0")}
        >
          0
        </button>
        <button className={styles.button} onClick={handleDecimal}>
          .
        </button>
        <button
          className={`${styles.button} ${styles.equals}`}
          onClick={handleEquals}
        >
          =
        </button>
      </div>
    </div>
  );
}
