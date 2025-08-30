export default function MicrosoftIcon({ size = 24, radius = 0 }) {
  // radius lets you slightly round the squares if you want
  const r = radius;
  const s = size;
  const g = s * 0.08; // gap
  const tile = (x, y, fill) => (
    <rect x={x} y={y} width={(s - g) / 2} height={(s - g) / 2} rx={r} ry={r} fill={fill} />
  );
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={s} height={s} viewBox={`0 0 ${s} ${s}`}>
      {tile(0, 0, "#F35325")}
      {tile((s + g) / 2, 0, "#81BC06")}
      {tile(0, (s + g) / 2, "#05A6F0")}
      {tile((s + g) / 2, (s + g) / 2, "#FFBA08")}
    </svg>
  );
}