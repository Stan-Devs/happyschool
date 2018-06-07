<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <b-container>
            <b-card :title="lastName + ' ' + firstName" no-body>
                <b-tabs card>
                    <b-tab title="Info générale" active>
                        <b-row>
                            <b-col cols="5">
                                <div>
                                    <b-img rounded fluid :src="photoPath" fluid alt="Photo de l'élève" />
                                </div>
                            </b-col>
                            <b-col>
                                <dl class="row">
                                    <dt class="col-sm-5 text-right">Nom </dt>
                                    <dd class="col-sm-7">{{ lastName }}</dd>
                                    <dt class="col-sm-5 text-right">Prénom </dt>
                                    <dd class="col-sm-7">{{ firstName }}</dd>
                                    <dt class="col-sm-5 text-right">Matricule</dt>
                                    <dd class="col-sm-7">{{ matricule }}</dd>
                                    <dt class="col-sm-5  text-right">Enseignement(s) </dt>
                                    <dd v-for="(t, index) in teachings" :key="t.id"
                                        :class="{'col-sm-7': index == 0, 'col-sm-7 offset-5': index > 0}">
                                        {{ t.display_name }}
                                    </dd>
                                    <dt class="col-sm-5  text-right">Classe(s) </dt>
                                    <dd v-for="(c, index) in classe" :key="c.id"
                                        :class="{'col-sm-7': index == 0, 'col-sm-7 offset-5': index > 0}">
                                        {{ c.year }}{{ c.letter.toUpperCase()}}
                                    </dd>
                                    <dt v-if="type === 'student'" class="col-sm-5 text-right">Date de naissance </dt>
                                    <dd v-if="type === 'student'" class="col-sm-7">{{ student_info.birth_date }}</dd>
                                    <dt v-if="type === 'student'" class="col-sm-5 text-right">Adresse </dt>
                                    <dd v-if="type === 'student'" class="col-sm-7">{{ student_info.street }}</dd>
                                    <dd v-if="type === 'student'" class="col-sm-7 offset-5">{{ student_info.postal_code }} – {{ student_info.locality }}</dd>

                                </dl>
                            </b-col>
                        </b-row>
                    </b-tab>
                    <b-tab title="Moyens de contacts" v-if="contact">
                        <dl class="row">
                            <dt class="col-sm-5 text-right">Nom du responsable</dt>
                            <dd class="col-sm-7">{{ contact.resp_last_name }} {{ contact.resp_first_name }}</dd>
                            <dt class="col-sm-5 text-right">Téléphone responsable</dt>
                            <dd class="col-sm-7">{{ contact.resp_phone }}</dd>
                            <dt class="col-sm-5 text-right">GSM responsable</dt>
                            <dd class="col-sm-7">{{ contact.resp_mobile }}</dd>
                            <dt class="col-sm-5 text-right">Email responsable</dt>
                            <dd class="col-sm-7"><a :href="'mailto:' + contact.resp_email">{{ contact.resp_email }}</a></dd>
                            <dt class="col-sm-5 text-right">Nom de la mère</dt>
                            <dd class="col-sm-7">{{ contact.mother_last_name }} {{ contact.mother_first_name }}</dd>
                            <dt class="col-sm-5 text-right">Téléphone de la mère</dt>
                            <dd class="col-sm-7">{{ contact.mother_phone }}</dd>
                            <dt class="col-sm-5 text-right">GSM de la mère</dt>
                            <dd class="col-sm-7">{{ contact.mother_mobile }}</dd>
                            <dt class="col-sm-5 text-right">Email de la mère</dt>
                            <dd class="col-sm-7"><a :href="'mailto:' + contact.mother_email">{{ contact.mother_email }}</a></dd>
                            <dt class="col-sm-5 text-right">Nom du père</dt>
                            <dd class="col-sm-7">{{ contact.father_last_name }} {{ contact.father_first_name }}</dd>
                            <dt class="col-sm-5 text-right">Téléphone du père</dt>
                            <dd class="col-sm-7">{{ contact.father_phone }}</dd>
                            <dt class="col-sm-5 text-right">GSM du père</dt>
                            <dd class="col-sm-7">{{ contact.father_mobile }}</dd>
                            <dt class="col-sm-5 text-right">Email du père</dt>
                            <dd class="col-sm-7"><a :href="'mailto:' + contact.father_email">{{ contact.father_email }}</a></dd>
                        </dl>
                    </b-tab>
                    <b-tab title="Info médicales" v-if="medical">
                        <dl class="row">
                            <dt class="col-sm-5 text-right">Médecin</dt>
                            <dd class="col-sm-7">{{ medical.doctor }}</dd>
                            <dt class="col-sm-5 text-right">Téléphone médecin</dt>
                            <dd class="col-sm-7">{{ medical.doctor_phone }}</dd>
                            <dt class="col-sm-5 text-right">Mutuelle</dt>
                            <dd class="col-sm-7">{{ medical.mutual }}</dd>
                            <dt class="col-sm-5 text-right">Numéro mutuelle</dt>
                            <dd class="col-sm-7">{{ medical.mutual_number }}</dd>
                            <dt class="col-sm-5 text-right">Infos complémentaires</dt>
                            <dd class="col-sm-7">{{ medical.medical_information }}</dd>
                        </dl>
                    </b-tab>
                </b-tabs>
            </b-card>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

export default {
    props: ['matricule', 'type'],
    data: function () {
        return {
            lastName: '',
            firstName: '',
            classe: [],
            teachings: [],
            student_info: {},
            contact: null,
            medical: null,
        }
    },
    computed: {
        photoPath: function () {
            let path = '/static/photos'
            if (this.type == 'responsible') path += '_prof';
            return path + '/' + this.matricule + '.jpg'
        }
    },
    watch: {
        matricule: function () {
            this.loadInfo();
        }
    },
    methods: {
        loadInfo: function () {
            this.contact = null;
            this.medical = null;

            if (this.type == 'student') {
                axios.get('/annuaire/api/student/' + this.matricule + '/')
                .then(response => {
                    this.lastName = response.data.last_name;
                    this.firstName = response.data.first_name;
                    this.classe = [response.data.classe];
                    this.teachings = [response.data.teaching];
                });

                axios.get('/annuaire/api/info_general/' + this.matricule + '/')
                .then(response => {
                    this.student_info = response.data;
                });

                axios.get('/annuaire/api/info_contact/' + this.matricule + '/')
                .then(response => {
                    this.contact = response.data;
                });

                axios.get('/annuaire/api/info_medical/' + this.matricule + '/')
                .then(response => {
                    this.medical = response.data;
                });
            } else if (this.type == 'responsible') {
                axios.get('/annuaire/api/responsible/' + this.matricule + '/')
                .then(response => {
                    this.lastName = response.data.last_name;
                    this.firstName = response.data.first_name;
                    this.classe = response.data.classe;
                    this.teachings = response.data.teaching;
                })
            }
        }
    },
    mounted: function () {
        this.loadInfo();
    }
}
</script>

<style>
</style>
