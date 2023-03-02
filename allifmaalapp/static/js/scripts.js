
class Calculator{
    constructor(previousTextElement, currentTextElement){
        this.previousTextElement = previousTextElement
        this.currentTextElement = currentTextElement
        this.clear()//as soon as you call this class, clear the screen
    }

    //create the calculator Functions
    clear(){
        
        this.current-number ==''
        this.previous-number ==''
        this.operation=undefined

    }
    delete(){

    }
    appendNumbers(Number){
        this.current-number == Number

    }
    chooseOperations(operation){


    }
    compute(){

    }
    updateDisplay(){
        this.currentTextElement.innerText=this.current-number

    }
}
const numberButtons=document.querySelectorAll(['data-number'])
const operationButtons=document.querySelectorAll(['data-operation'])
const equalsButtons=document.querySelector(['data-equals'])
const deleteButtons=document.querySelector(['data-delete'])
const allClearButtons=document.querySelector(['data-all-clear'])
const previousTextElement=document.querySelector(['data-previous-number'])
const currentTextElement=document.querySelector(['data-current-number'])

const calculator= new Calculator(previousTextElement, currentTextElement)
numberButtons.forEach(button => {
    button.addEventListener('click',()=>{
        calculator.appendNumbers(button.innerText)
        calculator.updateDisplay()
    })
})


// below is for testing only
function myFunction() {
    document.getElementById("demo").innerHTML = "Paragraph changed.";
  }