export default function PhoneIcon({ size = 24, strokeWidth = 2 }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 16.92v2a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h2a2 2 0 0 1 2 1.72c.12.9.34 1.77.67 2.6a2 2 0 0 1-.45 2.11L7.09 9.64a16 16 0 0 0 6 6l1.2-1.19a2 2 0 0 1 2.12-.46c.83.33 1.7.55 2.6.67A2 2 0 0 1 22 16.92z" />
    </svg>
  );
}