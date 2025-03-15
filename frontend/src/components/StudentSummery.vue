<template>
    <div>
        <student-navbar/>
        <div class="chart-container">
            <div class="chart-item bar-chart">
                <h2 class="text-center">Subject Wise No. of  Quizzes</h2><br>
                <p v-if="errorMessageBar" style="color: red;font-size: 20px;">{{ errorMessageBar }}</p>
                <canvas v-else ref="barChart"></canvas>
            </div>
            <div class="chart-item pie-chart">
                <h2 class="text-center">Subject Wise No. of  Quizzes Attempted</h2><br>
                <p v-if="errorMessagePie" style="color: red;font-size: 20px;">{{ errorMessagePie }}</p>
                <canvas v-else ref="pieChart"></canvas>
            </div>
        </div>
    </div>
</template>
  
<script>
import { Chart, registerables } from 'chart.js';
import StudentNavbar from './StudentNavbar.vue';
  Chart.register(...registerables);
  
  export default {
  components: { StudentNavbar },
    name: 'ChartComponent',
    data() {
      return {
        errorMessageBar:'',
        errorMessagePie:'',
        barChart: null,
        pieChart: null,
        sub_top_mark: {},
        sub_attempts: {},
        barChartData: {
          labels: [],
          datasets: [
            {
              data: [],
              label: '',
              backgroundColor: ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)','rgba(153, 102, 255, 0.2)'],
              borderColor: ['rgba(255, 99, 132, 1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)','rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)'],
              borderWidth: 1
            }
          ]
        },
        pieChartData: {
          labels: [],
          datasets: [
            {
              label: 'Distribution',
              data: [],
              backgroundColor: ['rgba(255, 159, 64, 0.2)','rgba(153, 102, 255, 0.2)','rgba(75, 192, 192, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 99, 132, 0.2)'],
              borderColor: ['rgba(255, 159, 64, 1)','rgba(153, 102, 255, 1)','rgba(75, 192, 192, 1)','rgba(54, 162, 235, 1)','rgba(255, 99, 132, 1)'],
              borderWidth: 1
            }
          ]
        }
      };
    },
    methods: {
      async fetchSubQuizzes() {
        try {
          const response = await fetch('/api/subject/num-quizzes', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('userToken')}`
            }
          });
          const result = await response.json();
          if (!response.ok) {
            this.errorMessageBar = result.message
            // alert(result.message);
          } else {
            this.errorMessageBar='',
            this.sub_top_mark = result;
            this.transformBarData();
            this.renderBarChart();
          }
        } catch (error) {
          console.error(error);
        }
      },
      async fetchSubAttempts() {
        try {
          const response = await fetch('/api/subject/attempt', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('userToken')}`
            }
          });
          const result = await response.json();
          if (!response.ok) {
            this.errorMessagePie = result.message
            // alert(result.message)
          } else {
            this.errorMessagePie = '';
            this.sub_attempts = result;
            this.transformPieData();
            this.renderPieChart();
          }
        } catch (error) {
          console.error(error);
        }
      },
      transformBarData() {
        const keys = Object.keys(this.sub_top_mark);
        const values = Object.values(this.sub_top_mark);
  
        this.barChartData.labels = keys;
        this.barChartData.datasets[0].data = values;
      },
      transformPieData() {
        const keys = Object.keys(this.sub_attempts);
        const values = Object.values(this.sub_attempts);
  
        this.pieChartData.labels = keys;
        this.pieChartData.datasets[0].data = values;
      },
      renderBarChart() {
        if (this.barChart) {
          this.barChart.destroy();
        }
        const ctx = this.$refs.barChart.getContext('2d');
        this.barChart = new Chart(ctx, {
          type: 'bar',
          data: this.barChartData,
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
      renderPieChart() {
        if (this.pieChart) {
          this.pieChart.destroy();
        }
        const ctx = this.$refs.pieChart.getContext('2d');
        this.pieChart = new Chart(ctx, {
          type: 'pie',
          data: this.pieChartData,
          options: {
            responsive: true
          }
        });
      }
    },
    mounted() {
      this.fetchSubQuizzes();
      this.fetchSubAttempts();
    }
  };
  </script>
  
  <style scoped>
  .chart-container {
    display: flex;
    justify-content: space-around;
    margin-top: 5%;
    margin-left: 5%;
  }
  .bar-chart canvas {
  width: 500px;
  height: 100px;
}

.pie-chart canvas {
  width: 200px;
  height: 400px;
}

  canvas {
    max-width: 600px;
    max-height: 600px;
    margin-bottom: 20px;
  }
  </style>
  