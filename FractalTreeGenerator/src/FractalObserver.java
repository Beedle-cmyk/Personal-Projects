/**
 * Observer interface where observers that implement this will be notified and updated
 *
 * @author beedle-cmyk
 * @version 12/6/2024
 */
public interface FractalObserver {
    /**
     * updates the list of fractal elements and repaints the display
     */
    public void update();
}