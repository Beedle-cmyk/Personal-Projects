import java.awt.*;
import java.util.ArrayList;

/**
 * Subject interface that allows for observers to receive updated fractal data
 *
 * @author     beedle-cmyk
 * @version    12/6/2024
 */
public interface FractalSubject {

    /**
     * Notifies all registered observers when there is a change
     */
    public void notifyObservers();

    /**
     * Registers an Observer
     * @param obs  Observer to be registered
     */
    public void registerObserver(FractalObserver obs);

    /**
     * Unregisters/removes an observer
     * @param obs  Observer to be removed/unregistered
     */
    public void unregisterObserver(FractalObserver obs);

    /**
     * sets the options (parameters) to adjust and generate the fractal
     *
     * @param sliderData  Array of slider data that adjusts/generates fractal
     * @param colorData   Array of color data that adjusts fractal color
     */
    public void setOptions(int[] sliderData, Color[] colorData);

    /**
     * returns the list of fractal elements
     *
     * @return  The list of fractal elements
     */
    public ArrayList<FractalElement> getFractalElements();
}