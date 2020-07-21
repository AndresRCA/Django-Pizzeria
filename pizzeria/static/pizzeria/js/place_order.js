class Pizza {
	constructor(size, toppings) {
		this.size = size // size object
		this.toppings = toppings // [Topping]
	}

  getTotal() {
    let total = 0.00
    total += this.size.price
    this.toppings.forEach(topping => {
      total += topping.price
    })
    return total
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
  	selected_size: {}, // size object
  	toppings: [], // toppings received from backend: {id, name, price}
  	selected_toppings: [],
  	pizzas: [] // array of Pizza objects
  },
  computed: {
  	size_price() {
  		return this.selected_size.price
  	},
    order_total() {
      let total = 0.00
      this.pizzas.forEach(pizza => {
        total += pizza.getTotal()
      })
      return total
    }
  },
  methods: {
    addTopping(id) {
      let topping = this.toppings.find(topping => topping.id == id)
      this.selected_toppings.push(topping)
    },
  	removeToppingFromSelected(index) {
  		this.selected_toppings.splice(index, 1)
  	},
  	addPizza() {
      let toppings_copy = Array.from(this.selected_toppings) // get shallow copy
      let pizza = new Pizza(this.selected_size, toppings_copy)
  		this.pizzas.push(pizza)
      console.log(pizza.getTotal())
  	},
    removePizza(index) {
      this.pizzas.splice(index, 1)
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
  		return "$" + Number.parseFloat(value).toFixed(2)
  	}
  },
  created() {
    this.sizes = sizes
    this.toppings = toppings
    this.selected_size = sizes[0]
  }
})