//
//  ResultViewController.swift
//  Tips Calculator
//
//  Created by Ru Yang on 8/19/21.
//

import UIKit

class ResultViewController: UIViewController {
    
    @IBOutlet weak var detailLabel: UILabel!
    @IBOutlet weak var resultLabel: UILabel!
    var splitValue: String?
    var tipValue: String?
    var result: String?

    override func viewDidLoad() {
        super.viewDidLoad()
        resultLabel.text = "$ \(result!)"
        detailLabel.text = "Split Between \(splitValue!) People, with \(tipValue!) tip."
    }
    
    @IBAction func recalculatePressed(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
    
}
