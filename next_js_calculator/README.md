# Next.js Interactive Calculator

A beautiful, fully functional calculator built with Next.js 14, TypeScript, and CSS Modules. This calculator runs entirely on the client side using React hooks for state management.

## Features

- ✨ Modern, gradient-based UI design
- 🔢 Basic arithmetic operations (addition, subtraction, multiplication, division)
- 🎯 Additional functions (percentage, toggle sign, clear)
- 📱 Fully responsive design
- ⚡ Client-side only (no server-side rendering needed)
- 🎨 Smooth animations and transitions
- 💯 TypeScript for type safety

## Operations Supported

- Addition (+)
- Subtraction (-)
- Multiplication (×)
- Division (÷)
- Percentage (%)
- Toggle Sign (+/-)
- Clear (AC)
- Decimal numbers

## Getting Started

### Prerequisites

Make sure you have Node.js installed (version 18 or higher recommended).

### Installation

1. Install dependencies:

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the calculator.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
next_js_calculator/
├── app/
│   ├── layout.tsx          # Root layout component
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── Calculator.tsx      # Calculator component (client-side)
│   └── Calculator.module.css # Calculator styles
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── README.md
```

## Technology Stack

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **CSS Modules** - Scoped styling
- **Tailwind CSS** - Utility-first CSS framework

## How It Works

The calculator uses React's `useState` hook to manage:

- Current display value
- Previous value (for operations)
- Selected operation
- Display reset state

All calculations are performed client-side using the `'use client'` directive, ensuring fast, responsive interactions without any server round-trips.

## Keyboard Support

Currently supports mouse/touch input. Keyboard support can be added in future updates.

## Browser Support

Works in all modern browsers that support ES6+ and React 18.

## License

MIT

## Author

Created as a learning project for Next.js and React development.
