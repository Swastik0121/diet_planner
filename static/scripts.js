class TextAnimator {
    constructor(selector, options) {
        this.text = document.querySelector(selector);
        this.strText = this.text.textContent.trim();
        this.splitText = this.strText.split("");
        this.text.textContent = "";
        this.options = options || {};
        this.margin = this.options.margin || '0px';
        this.delay = this.options.delay || 0;
        this.class = this.options.class || 'text-span';
    }

    animate() {
        for (let i = 0; i < this.splitText.length; i++) {
            if (this.splitText[i] === " ") {
                this.text.innerHTML += "&nbsp;";
            } else {
                this.text.innerHTML += "<span class='"+ this.class + "' style='margin-right:" + this.margin + ";animation-delay:" + (i * this.delay) + "ms;'><span class='fade-in' style='animation-delay:" + (i * this.delay) + "ms;'>" + this.splitText[i] + "</span></span>";
            }
        }
    }
    
}

const animator = new TextAnimator('.text-blob', {
    margin: '5px',
    delay: 100,
    class: "text-blob__letter"
});
animator.animate();

document.getElementById("recommend").addEventListener("click", function(event) {
    const form = document.getElementById('form');

    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;
    const disease = document.getElementById('disease').value;
    const region = document.getElementById('region').value;
    const allergics = document.getElementById('allergics').value;

    let valid = true;

    if (!age || age < 10 || age > 90) {
        valid = false;

    }

    if (!height || height < 120 || height > 250) {
        valid = false;
    }

    if (!weight || weight < 30 || weight > 200) {
        valid = false;
    }

    if (!region) {
        valid = false;
    }

    if (!allergics) {
        valid = false;
    }

    if (!disease) {
        valid = false;
    }

    if (valid){
        form.submit();
    }
});