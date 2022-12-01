<template>
    <vue-cal 
        class="vuecal__dark-blue-theme"
        events-count-on-year-view
        events-on-month-view="short"
        :time-from="8 * 60"
        :time-to="21 * 60"
        :snap-to-time="30"
        :time-step="30"
        :editable-events="{ title: false, drag: false, resize: true, delete: true, create: true }"
        :on-event-create="onEventCreate"
        :on-event-click="onEventClick"
        :min-date="minDate"
        :events="this.events"
        @event-drag-create="showEventDialog = true"
    >

    </vue-cal>
    <q-dialog v-model="showEventDialog"  :no-esc-dismiss=true max-width="420">
        <q-card>
            <q-card-section>
                <q-input 
                    color="primary"
                    v-model="selectedEvent.title"
                    label="Title" 
                />
                <div 
                    class="text-subtitle2 q-my-none text-weight-regular"
                >
                    Start date
                </div>
                <div 
                    class="text-weight-bold q-my-none text-weight-regular"
                >
                    {{selectedEvent.start.toLocaleTimeString([], {year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false})}}
                </div>
                <div class="text-subtitle2 q-my-none text-weight-regular"
                >
                    End date
                </div>
                <div 
                    class="text-weight-bold q-my-none text-weight-regular"
                >
                    {{selectedEvent.end.toLocaleTimeString([], {year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false})}}
                </div>
                <q-input
                    color="primary"
                    v-model="selectedEvent.content"
                    filled
                    type="textarea"
                    label="Description"
                />
            </q-card-section>
            <q-card-actions align="right" class="text-primary">
                <q-btn 
                    flat
                    color="primary" 
                    label="Cancel" 
                    @click="cancelEventCreation()"
                />
                <q-btn
                    v-if="this.editEvent"
                    flat
                    color="primary" 
                    label="Update" 
                    @click="closeCreationDialog('modified')"
                />
                <q-btn
                    v-if="this.editEvent"
                    flat
                    color="primary" 
                    label="Delete" 
                    @click="closeCreationDialog('canceled')"
                />
                <q-btn
                    v-if="this.editEvent != true"
                    flat
                    color="primary" 
                    label="Save" 
                    @click="closeCreationDialog('created')"
                />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
  
<script>
    import { useQuasar } from 'quasar'
    import { defineComponent } from 'vue'
    import { mapActions } from 'vuex'
    import VueCal from 'vue-cal'
    import 'vue-cal/dist/vuecal.css'

    let $q
    
    export default defineComponent({
        name: 'MeetingCalendar',
        components: { VueCal },
        data: () => ({
            selectedEvent: {title: '', content: ''},
            showEventDialog: false,
            editEvent: false,
            events: [],
        }),
        methods: {
            onEventClick (event, e) {
                this.selectedEvent = event;
                this.showEventDialog = true;
                this.editEvent = true;
                // Prevent navigating to narrower view (default vue-cal behavior).
                e.stopPropagation();
            },
            onEventCreate (event, deleteEventFunction) {
                this.selectedEvent = event;
                this.showEventDialog = true;
                this.deleteEventFunction = deleteEventFunction;

                return event;
            },
            cancelEventCreation () {
                this.editEvent = false;
                this.showEventDialog = false;
                this.selectedEvent = {};
                this.deleteEventFunction();
            },
            ...mapActions('meeting', ['putEvent']),
            ...mapActions('meeting', ['postEvent']),
            async closeCreationDialog (status) {
                try {
                    let edited_event = {
                        token: this.$store.state.auth.token,
                        title: this.selectedEvent.title,
                        description: this.selectedEvent.content,
                        start_dt: this.toUTCDateTime(this.selectedEvent.start),
                        end_dt: this.toUTCDateTime(this.selectedEvent.end),
                        status: status
                    };
                    if (status === "created") {
                        await this.postEvent(edited_event);
                    } else {
                        edited_event.id = this.selectedEvent.id;
                        await this.putEvent(edited_event);
                    }
                } catch (err) {
                    if (err.response.data.detail) {
                        $q.notify({
                            type: 'negative',
                            message: err.response.data.detail
                        });
                    }
                }
                this.editEvent = false;
                this.showEventDialog = false;
                this.selectedEvent = {};
                this.events = [];
                this.getMeeting();
            },
            ...mapActions('meeting', ['getEvents']),
            async getMeeting () {
                try {
                    await this.getEvents(this.$store.state.auth.token);
                    let data = this.$store.state.meeting.events;
                    this.events = this.processingData(
                        data
                    );
                } catch (err) {
                    if (err.response.data.detail) {
                        $q.notify({
                            type: 'negative',
                            message: err.response.data.detail
                        });
                    }
                }
            },
            processingData (data) {
                let events = [];
                for (let i = 0; i < data.own_meetings.length; i++) {
                    events.push(
                        {
                            id: data.own_meetings[i].id,
                            title: data.own_meetings[i].title,
                            content: data.own_meetings[i].description,
                            start: new Date(data.own_meetings[i].start_dt + '.000Z'),
                            end: new Date(data.own_meetings[i].end_dt + '.000Z')
                        }
                    );
                }
                for (let i = 0; i < data.other_client_meetings.length; i++) {
                    events.push(
                        {
                            id: data.other_client_meetings[i].id,
                            title: "Booked",
                            content: '<i class="icon material-icons">block</i><br>Booked',
                            start: new Date(data.other_client_meetings[i].start_dt + '.000Z'),
                            end: new Date(data.other_client_meetings[i].end_dt + '.000Z'),
                            class: "vuecal__disable-pointer",
                            deletable: false,
                            resizable: false,
                            draggable: false
                        }
                    );
                }
                return events
            },
            toUTCDateTime (date) {
                return date.getUTCFullYear() + "-" + (date.getUTCMonth() + 1) +
                     "-" + date.getUTCDate() + " " + date.getUTCHours() + ":" +
                     String(date.getMinutes()).padStart(2, '0');
            }
        },
        computed: {
            minDate () {
                return new Date();
            }
        },
        beforeMount(){
            this.getMeeting();
        },
        mounted () {
            $q = useQuasar();
        }
    })
</script>

<style>
    #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    }

    .vuecal {height: 90vh;}
</style>