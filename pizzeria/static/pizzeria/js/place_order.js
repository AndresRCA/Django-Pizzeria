class Pizza {
	constructor(size, toppings) {
		this.size = size // size id
		this.toppings = toppings // [Topping]
	}

  getToppingNames() {
    let topping_names = this.toppings.map(topping => topping.name)
    return topping_names
  }
}

var app = new Vue({
	delimiters: ['[[', ']]'],
  el: '#app',
  data: {
  	sizes: [], // sizes received from backend: {id, name, price}
  	selected_size: 1, // id representing the size
  	toppings: [], // toppings received from backend: {id, name, price}
  	selected_toppings: [],
  	pizzas: [] // array of Pizza objects
  },
  computed: {
  	size_price() {
  		let size = this.sizes.find(size => size.id == this.selected_size)
  		return size.price
  	}
  },
  methods: {
    addTopping(id) {
      let topping = this.toppings.find(topping => topping.id == id)
      this.selected_toppings.push(topping)
    },
  	removeToppingFromSelected(index) {
      console.log('is it working?')
  		this.selected_toppings.splice(index, 1)
  	},
  	addPizza() {
  		let pizza = new Pizza(this.selected_size, this.selected_toppings)
  		this.pizzas.push(pizza)
  	}
  },
  filters: {
  	capitalize(value) {
  		if (!value) return ''
  		value = value.toString()
  		return value.charAt(0).toUpperCase() + value.slice(1)
  	},
  	currency(value) {
  		if (!value) return ''
  		return Number.parseFloat(value).toFixed(2) + "$"
  	}
  },
  created() {
  	console.log('Vue instance been created successfully')
    this.sizes = sizes
    this.toppings = toppings
  }
})