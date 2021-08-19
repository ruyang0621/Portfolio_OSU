//
//  ViewController.swift
//  Tips Calculator
//
//  Created by Ru Yang on 8/18/21.
//

import UIKit

class CalculatorViewController: UIViewController {

    @IBOutlet weak var textField: UITextField!
    @IBOutlet weak var tipSlider: UISlider!
    @IBOutlet weak var splitSlider: UISlider!
    @IBOutlet weak var tipLabel: UILabel!
    @IBOutlet weak var splitLabel: UILabel!
    
    var calculatorSplitAmount = CalculatorSplitAmount()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tipSlider.value = 15
        splitSlider.value = 3
    }
    
    // Changes the Tip Slider to change the Tip Label.
    @IBAction func tipSliderChanged(_ sender: UISlider) {
        let tipVal = String(format: "%.0f", sender.value)
        tipLabel.text = "\(tipVal)%"
    }
    
    
    // Changes the Split Slider to change the Split Label.
    @IBAction func splitSliderChanged(_ sender: UISlider) {
        splitLabel.text = String(format: "%.0f", sender.value)
    }
    
    
    // Press the Calculate button.
    @IBAction func calculatePressed(_ sender: UIButton) {
        // Calculate the Result.
        let tipPercentage = tipSlider.value.rounded() / 100
        let splitNum = splitSlider.value.rounded()
        var amount:Float
        
        if textField.text == ""{
            amount = 150
        } else {
            amount = Float(textField.text!)!
        }
        
        calculatorSplitAmount.calculatorResult(amount: amount, tipPercentage: tipPercentage, splitNum: splitNum)
       
        // Go to the result Scene.
        self.performSegue(withIdentifier: "goToResult", sender: self)
    }
    
    
    // Prepare function for navigation override.
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "goToResult" {
            let destinationVC = segue.destination as! ResultViewController
            destinationVC.splitValue = splitLabel.text
            destinationVC.tipValue = tipLabel.text
            destinationVC.result = calculatorSplitAmount.getResult()
        }
    }
    
    // Hides the Keyboard when touch the screen.
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
    
}


