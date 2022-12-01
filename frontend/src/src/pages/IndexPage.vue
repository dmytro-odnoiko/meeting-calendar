<template>
  <q-page>
    <MeetingCalendar/>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import MeetingCalendar from '../components/Calendar.vue'

export default defineComponent({
  name: 'IndexPage',
  components: { MeetingCalendar }
})
</script>
