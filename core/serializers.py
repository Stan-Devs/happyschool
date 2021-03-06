# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers

from core.models import *


class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'last_name', 'first_name', 'is_secretary', 'email', 'email_alias', 'teaching')
        depth = 1


class ResponsibleSensitiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'matricule', 'last_name', 'first_name', 'is_secretary', 'email_alias',
                  'teaching', 'classe', 'tenure')
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = ('matricule', 'first_name', 'last_name', 'display', 'classe', 'teaching', 'user',)
        depth = 1


class StudentGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student', 'gender', 'scholar_year', 'previous_classe',
                  'orientation', 'birth_date', 'street', 'postal_code',
                  'locality', 'username', 'password')


class StudentContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student',
                  'student_phone', 'student_mobile', 'student_email',
                  'resp_last_name', 'resp_first_name', 'resp_phone', 'resp_mobile', 'resp_email',
                  'mother_last_name', 'mother_first_name', 'mother_phone', 'mother_mobile', 'mother_email',
                  'father_last_name', 'father_first_name', 'father_phone', 'father_mobile', 'father_email',
                  )


class StudentMedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student', 'doctor', 'doctor_phone', 'mutual', 'mutual_number', 'medical_information')


class ClasseSerializer(serializers.ModelSerializer):
    display = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = ClasseModel
        fields = '__all__'


class TeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingModel
        fields = '__all__'
