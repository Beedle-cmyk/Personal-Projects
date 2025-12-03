import java.awt.*;
/**
 * Interface that allows for different types of fractal elements to be drawn by
 * the FractalDrawing class via a branch Record
 *
 * @author   beedle-cmyk
 * @version  12/6/2024
 */
public interface FractalElement {

    /**
     * Constructs a fractal through the graphics object
     *
     * @param g        Graphics object instantiated
     */
    public void draw(Graphics g);
}