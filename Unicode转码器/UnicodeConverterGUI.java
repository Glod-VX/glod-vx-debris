package jmq;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class UnicodeConverterGUI {

    public static void main(String[] args) {
        // 创建主窗口
        JFrame frame = new JFrame("Unicode 码互译器");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 200);

        // 创建面板
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(3, 2));

        // 标签
        JLabel inputLabel = new JLabel("输入字符或Unicode编码:");
        JLabel resultLabel = new JLabel("转换结果:");

        // 输入字段
        JTextField inputField = new JTextField();
        JTextField resultField = new JTextField();
        resultField.setEditable(false);  // 结果字段不可编辑

        // 按钮
        JButton toUnicodeButton = new JButton("字符转Unicode编码");
        JButton toCharButton = new JButton("Unicode编码转字符");

        // 按钮事件处理
        toUnicodeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String input = inputField.getText();
                if (input.length() == 1) {
                    char ch = input.charAt(0);
                    String unicode = "\\u" + Integer.toHexString(ch | 0x10000).substring(1);
                    resultField.setText(unicode);
                } else {
                    JOptionPane.showMessageDialog(frame, "请输入一个字符！", "错误", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        toCharButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String input = inputField.getText();
                try {
                    int codePoint = Integer.parseInt(input, 16);
                    char character = (char) codePoint;
                    resultField.setText(Character.toString(character));
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "请输入有效的Unicode编码！", "错误", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        // 将组件添加到面板
        panel.add(inputLabel);
        panel.add(inputField);
        panel.add(resultLabel);
        panel.add(resultField);
        panel.add(toUnicodeButton);
        panel.add(toCharButton);

        // 添加面板到框架
        frame.getContentPane().add(panel);
        frame.setVisible(true);
    }
}
