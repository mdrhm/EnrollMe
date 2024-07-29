let total_revenue, revenue_by_service, order_by_service, order_by_service_by_month
const colors = ["#00a6a1", "#006db3", "#0035c5", "#3a35cf", "#8ac926", "#7536d9", "#e67d3b", "#bd9853", "#95b36c"]

const getReports = new XMLHttpRequest();
getReports.withCredentials = true;
getReports.addEventListener("readystatechange", function() {
    if(this.readyState === 4) {
        if(this.status == 200){
            let reports = JSON.parse(this.responseText)
            total_revenue = reports["total_revenue"]
            revenue_by_service = reports["revenue_by_service"]
            order_by_service = reports["order_by_service"]
            order_by_service_by_month = reports["order_by_service_by_month"]
            Chart.defaults.color = '#ffffff';
            loadRevenueByService()
            loadTotalOrdersByService()
            loadOrderByServiceByMonth()
            showRevenue(total_revenue.at(-1)["total_revenue"])
        }
    }
});
getReports.open("POST", "/revenue/download");
getReports.setRequestHeader("Content-Type", "application/json");
getReports.send("");

function loadRevenueByService() {
    const data = {
        responsive: true,
        maintainAspectRatio: false,
        width: 550,
        height: 550,
        labels: revenue_by_service.map((service) => {return service["name"] + " - " + service["type"]}),
        datasets: [{
            data: revenue_by_service.map((service) => {return (service["total"]) ? parseFloat(service["total"]) : 0}),
            backgroundColor: colors.map((color) => {return color + "77"}),
            hoverBackgroundColor: colors,
            hoverOffset: 4,
            borderColor: colors,
        }]
    }
    var options = {
        animation: {
            duration: 3000,
        }
    }
    new Chart('revenue-by-each-service', {
        type: 'doughnut',
        data: data,
        options: options
    });
}

function loadTotalOrdersByService() {
    var data = {
        labels: order_by_service.map((service) => {return service["name"] + " - " + service["type"]}),
        datasets: [{
            data: order_by_service.map((service) => {return service["count"]
            }),
            backgroundColor: colors.map((color) => {return color + "77"}),
            hoverBackgroundColor: colors,
            borderColor: colors,
            borderWidth: 2,
            hoverBorderColor: colors,
            color: "rgba(256,256,256)",
            hoverOffset: 4,
        }]
    };
    var options = {
        maintainAspectRatio: false,
        scales: {
            yAxes:  [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Y axis name',
                    fontColor: '#000000',
                    fontSize: 10
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 14
                }
            }]
        },
        animation: {
            y: {
                duration: 3000,
                from: 500
            }
        },
        plugins: {
            colors: {
                forceOverride: false
            }
        },
        legend: {
            display: false
        },
    };

    new Chart('total-orders-by-service', {
        type: 'bar',
        options: options,
        data: data
    });
}

function loadOrderByServiceByMonth() {
    let datasets = []
    for (let i = 0; i < order_by_service_by_month.length; i++){
        let service = order_by_service_by_month[i]
        let values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        let valuesToFilter = service["orders_by_month"].map((order) => {
            return order["count"]
        })
        let monthsToFilter = service["orders_by_month"].map((order) => {
            return parseInt(order["month"].split("-")[1])
        })
        console.log(monthsToFilter)
        for (let i = 0; i < valuesToFilter.length; i++) {
            values[monthsToFilter[i] - 1] = valuesToFilter[i]
        }
        console.log(values)
        let color = colors[i]
        console.log(color)
        datasets.push({
            label: service["name"] + " - " + service["type"],
            backgroundColor: color + "33",
            borderColor: color,
            borderWidth: 2,
            hoverBackgroundColor: color + "66",
            hoverBorderColor: color,
            color: "rgba(256,256,256)",
            data: values,
        })
    }
    var data = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: datasets
    };
    var options = {
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: "time",
                gridLines : {
                    display : false
                },
                scaleLabel : { fontColor: 'white', fontSize:16 }
            }],
        },
        animation: {
            y: {
                duration: 3000,
                from: 500
            }
        },
        legend: {
            labels: {
                color: 'white'
            }
        },
        plugins: {
            legend: {
                labels: {
                    font: {
                        color: 'white'
                    }
                }
            }
        }
    };

    new Chart('order-service-by-month', {
        type: 'line',
        options: options,
        data: data
    });
}

function showRevenue(revenue){
    const specialChars = [".", ",", "$"]
    const widths = {"0":55,"1":39,"2":50,"3":53,"4":54,"5":52,"6":53,"7":48,"8":53,"9":53,".":24,",":24,"$":52}
    document.querySelector(".total-revenue").innerHTML = ''
    for(let c of revenue){
        document.querySelector(".total-revenue").innerHTML += `<div class="number" style="--number: ${(specialChars.includes(c)) ? specialChars.indexOf(c) + 4 : parseInt(c) - 6}; width: ${widths[c]}px"> <h1>0</h1> <h1>1</h1> <h1>2</h1> <h1>3</h1> <h1>4</h1> <h1>5</h1> <h1>6</h1> <h1>7</h1> <h1>8</h1> <h1>9</h1> <h1>.</h1><h1>,</h1><h1>$</h1></div>`
    }
}


let scrollTimeout;

function scrollDown(){
    if (scrollTimeout) {
        return
    }
    lastKnownScrollPosition = window.scrollY;
    let option = (parseInt(getComputedStyle(document.querySelector(".revenue-container-inner")).getPropertyValue('--option')) + 1) % 4
    document.querySelector(".revenue-container-inner").style = "--option: " + option
    switch (option) {
        case 0:
            showRevenue(total_revenue.at(-1)["total_revenue"])
            break
        case 1:
            loadRevenueByService()
            break
        case 2:
            loadTotalOrdersByService()
            break
        case 3:
            loadOrderByServiceByMonth()
            break
    }
    console.log(lastKnownScrollPosition)
    scrollTimeout = setTimeout(() => {
        scrollTimeout = null
    }, 2000)
}

document.addEventListener("wheel", scrollDown)
document.querySelector(".scroll-arrow").addEventListener("click", scrollDown)