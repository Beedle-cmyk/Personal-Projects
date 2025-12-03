import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

/**
 * This is responsible for drawing and displaying the fractal using the fractal data in an ArrayList
 *
 * @author   beedle-cmyk
 * @version  12/6/2024
 */
public class FractalDrawing extends JFrame implements FractalObserver {
    /** Fractal Subject object for communication */
    private FractalSubject subject;

    /** fractal element data stored within the list from the subject */
    private ArrayList<FractalElement> fractalElements = new ArrayList<FractalElement>();

    /**
     * Constructor that builds/initializes the fractal display and sets up observer relationship
     *
     * @param subject   Fractal Subject object used to get the fractal elements
     */
    public FractalDrawing(FractalSubject subject) {
        this.subject = subject;
        subject.registerObserver(this);

        setTitle("Fractal Display");
        setBounds(400, 50, 1100, 800);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JPanel panel = new DrawArea();
        panel.setBackground(Color.black);
        getContentPane().add(panel);

        setVisible(true);
        update();
    }

    /**
     * updates the list of fractal elements and repaints the display
     */
    @Override
    public void update() {
        fractalElements = subject.getFractalElements();
        repaint();
    }

    /**
     * Inner private class that defines the area for drawing the fractal
     */
    private class DrawArea extends JPanel {

        /**
         * Constructor for DrawArea
         */
        public DrawArea(){
            //Does Nothing
        }

        /**
         * Constructor for draw area class that initializes the panel for fractal element use
         *
         * @param g the <code>Graphics</code> object to protect
         */
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            for (FractalElement element : fractalElements) {
                element.draw(g);
            }
        }
    }
}