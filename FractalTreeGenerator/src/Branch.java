import java.awt.*;
/**
 * Record for storing and utilizing Branch data
 *
 * @author   beedle-cmyk
 * @version  12/6/2024
 *
 * @param x1         The initial x position of the branch
 * @param y1         The initial y position of the branch
 * @param x2         The final x position of the branch
 * @param y2         The final y position of the branch
 * @param thickness  The thickness of the branch
 * @param color      The color of the branch
 *
 */
public record Branch(int x1, int y1, int x2, int y2, int thickness, Color color) implements FractalElement {

    /**
     * Constructs a fractal through the graphics object
     *
     * @param g  Graphics object instantiated
     */
    @Override
    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;

        Stroke s = new BasicStroke(thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND);
        g2.setStroke(s);

        g2.setColor(color);
        g2.drawLine(x1, y1, x2, y2);
    }
}