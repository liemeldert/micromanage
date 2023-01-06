import React, { useRef, useEffect } from 'react';

export default 
function FlowingGradientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;

    // Check if the canvas element exists
    if (canvas) {
      const ctx = canvas.getContext('2d');

      // Create a gradient that flows from top left to bottom right at a 45 degree angle
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, 'magenta');
      gradient.addColorStop(0.5, 'blue');
      gradient.addColorStop(1, 'red');

      // Fill the canvas with the gradient
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Animate the gradient by shifting the starting and ending points
      // to the right and down by a small amount each frame
      let x = 0;
      let y = 0;
      const xDelta = 1;
      const yDelta = 1;
      function animate() {
        x += xDelta;
        y += yDelta;
        gradient.addColorStop(0, 'magenta');
        gradient.addColorStop(0.5, 'blue');
        gradient.addColorStop(1, 'red');
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        requestAnimationFrame(animate);
      }
      animate();
    }
  }, []);

  return (
    <canvas
      ref={canvasRef}
      width={window.innerWidth}
      height={window.innerHeight}
    />
  );
}
