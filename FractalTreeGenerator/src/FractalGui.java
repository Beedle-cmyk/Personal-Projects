import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

/**
 * this class is responsible for gathering user data via the settings dialog.  When the user changes
 * any settings, all settings information is sent to the Subject (real-time updates).
 *
 * @author beedle-cmyk
 * @version 12/6/2024
 */
public class FractalGui extends JFrame {

    /** subject object for communication*/
    private FractalSubject subject;
    /** List of slider data settings e.g. recursion depth */
    private int[] sliderData;
    /** List of Color data */
    private Color[] colorData;

    /**
     * Base constructor for creation of the settings GUI. Includes buttons and sliders.
     *
     * @param subject   The subject object for data to be sent to
     */
    public FractalGui(FractalSubject subject) {
        sliderData = new int[] {12, 70, 20, 30, 200, 15};
        colorData = new Color[] {Color.YELLOW, new Color(160, 32, 240)};
        subject.setOptions(sliderData, colorData);

        this.subject = subject;
        setTitle("Fractal Settings");
        setBounds(60, 60, 280, 680);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(null);
        getContentPane().add(mainPanel);

        //RecursionDepth
        buildLabel(mainPanel,"Recursion Depth", 75, 30, 100, 20);
        JSlider recursionDepthSlider = buildSlider(mainPanel, 30, 50, 200, 45, 4, 20,
                12, 0, 2, 1);

        //Child to Parent Ratio
        buildLabel(mainPanel, "Child to parent ratio", 75, 100, 120, 20);
        JSlider childToParentRatioSlider = buildSlider(mainPanel, 30, 120, 200, 45, 40,
                80, 70, 1, 10, 5);

        //Left Child Angle
        buildLabel(mainPanel, "Left child angle", 75, 170, 100, 20);
        JSlider leftChildAngleSlider = buildSlider(mainPanel, 30, 190, 200, 45, 0, 90,
                20, 2, 10, 5);

        //Right Child Angle
        buildLabel(mainPanel, "Right child angle", 75, 240, 100, 20);
        JSlider rightChildAngleSlider = buildSlider(mainPanel, 30, 260, 200, 45, 0, 90,
                30, 3, 10, 5);

        //Trunk Length
        buildLabel(mainPanel, "Trunk length", 75, 310, 100, 20);
        JSlider trunkLengthSlider = buildSlider(mainPanel, 30, 330, 200, 45, 100,
                400, 200, 4, 100, 25);

        //Trunk Width
        buildLabel(mainPanel, "Trunk width", 75, 380, 100, 20);
        JSlider trunkWidthSlider = buildSlider(mainPanel, 30, 400, 200, 45, 10, 50,
                15, 5, 10, 5);

        //Trunk Button
        buildButton(mainPanel, "Trunk Color...", 75, 450, 115, 30, 1);

        //Leaf Button
        buildButton(mainPanel, "Leaf Color...", 75, 500, 110, 30, 0);

        //Randomization
        JButton randomizeButton = new JButton("Randomize");
        randomizeButton.setBounds(75, 550, 110, 30);
        mainPanel.add(randomizeButton);

        randomizeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Random random = new Random();
                sliderData[0] = random.nextInt(16) + 4;
                sliderData[1] = random.nextInt(40) + 40;
                sliderData[2] = random.nextInt(90);
                sliderData[3] = random.nextInt(90);
                sliderData[4] = random.nextInt(300) + 100;
                sliderData[5] = random.nextInt(40) + 10;
                colorData[0] = new Color(random.nextInt(255), random.nextInt(255),
                        random.nextInt(255));
                colorData[1] = new Color(random.nextInt(255), random.nextInt(255),
                        random.nextInt(255));
                subject.setOptions(sliderData, colorData);

                recursionDepthSlider.setValue(sliderData[0]);
                childToParentRatioSlider.setValue(sliderData[1]);
                leftChildAngleSlider.setValue(sliderData[2]);
                rightChildAngleSlider.setValue(sliderData[3]);
                trunkLengthSlider.setValue(sliderData[4]);
                trunkWidthSlider.setValue(sliderData[5]);
            }
        });
        setVisible(true);
    }

    /**
     * Constructs a label on the Fractal Settings GUI
     *
     * @param panel    The panel to be edited/updated
     * @param label    The Label name
     * @param x        The x position of the label
     * @param y        The y position of the label
     * @param width    The width of the label
     * @param height   The height of the label
     */
    private void buildLabel(JPanel panel, String label, int x, int y, int width, int height) {
        JLabel newLabel = new JLabel(label);
        newLabel.setBounds(x, y, width, height);
        panel.add(newLabel);
    }

    /**
     * Constructs a slider on the Fractal Settings GUI
     *
     * @param panel    The panel to be edited/updated
     * @param x        The x position of the slider
     * @param y        The y position of the slider
     * @param width    The width of the slider
     * @param height   The height of the slider
     * @param min      The minimum value that can be selected
     * @param max      The maximum value that can be selected
     * @param value    The default value of the slider
     * @param slot     position to be stored in sliderData
     * @param majSpace The distance between each major tick mark
     * @param minSpace The distance between each minor tick mark
     * @return         The slider built
     */
    private JSlider buildSlider(JPanel panel, int x, int y, int width, int height,
                             int min, int max, int value, int slot, int majSpace, int minSpace) {
        JSlider slider = new JSlider(SwingConstants.HORIZONTAL, min, max, value);
        slider.setBounds(x, y, width, height);
        slider.setMinorTickSpacing(minSpace);
        slider.setMajorTickSpacing(majSpace);
        slider.setSnapToTicks(true);
        slider.setPaintTicks(true);
        slider.setPaintLabels(true);
        panel.add(slider);

        slider.addChangeListener(new ChangeListener() {
            @Override
            public void stateChanged(ChangeEvent e) {
                sliderData[slot] = slider.getValue();
                subject.setOptions(sliderData, colorData);
            }
        });
        return slider;
    }

    /**
     * Builds buttons for selecting colors on Fractal Settings GUI
     *
     * @param panel    The panel to be edited/updated
     * @param label    The name of the button
     * @param x        The x position of the button
     * @param y        The y position of the button
     * @param width    The width of the button
     * @param height   The height of the button
     * @param slot     The position to be stored within colorData
     */
    private void buildButton(JPanel panel, String label, int x, int y, int width, int height, int slot) {
        JButton button = new JButton(label);
        button.setBounds(x, y, width, height);
        panel.add(button);
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Color colorChosen = JColorChooser.showDialog(FractalGui.this, "Choose " + label,
                        colorData[slot]);
                if (colorChosen != null) {
                    colorData[slot] = colorChosen;
                    subject.setOptions(sliderData, colorData);
                }
            }
        });
    }
}