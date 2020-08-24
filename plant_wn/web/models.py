# SPDX-License-Identifier: GPL-3.0-or-later
import bcrypt
import sqlalchemy
import sqlalchemy.orm
from werkzeug.exceptions import Unauthorized

from plant_wn.exceptions import ValidationError
from plant_wn.web import db


class Threshold:
    """A base class for a threshold."""

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    enabled = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.Float, nullable=False)


class MaxPrecipitation(db.Model, Threshold):
    """A max precipitation threshold."""

    __tablename__ = "max_precipitations"


class MinTemp(db.Model, Threshold):
    """A minimum temperature threshold."""

    __tablename__ = "min_temps"


class MaxTemp(db.Model, Threshold):
    """A maximum temperature threshold."""

    __tablename__ = "max_temps"


class MaxWind(db.Model, Threshold):
    """A maximum temperature threshold."""

    __tablename__ = "max_winds"


class Plant(db.Model):
    """A plant that is tied to a location and thresholds."""

    __tablename__ = "plants"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    max_precipitation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("max_precipitations.id"), nullable=True
    )
    max_temp_id = sqlalchemy.Column(sqlalchemy.ForeignKey("max_temps.id"), nullable=True)
    min_temp_id = sqlalchemy.Column(sqlalchemy.ForeignKey("min_temps.id"), nullable=True)
    max_wind_id = sqlalchemy.Column(sqlalchemy.ForeignKey("max_winds.id"), nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("users.id"))
    zip_code_id = sqlalchemy.Column(sqlalchemy.ForeignKey("zip_codes.id"), nullable=True)

    max_precipitation = sqlalchemy.orm.relationship("MaxPrecipitation", uselist=False)
    max_temp = sqlalchemy.orm.relationship("MaxTemp", uselist=False)
    min_temp = sqlalchemy.orm.relationship("MinTemp", uselist=False)
    max_wind = sqlalchemy.orm.relationship("MaxWind", uselist=False)
    user = sqlalchemy.orm.relationship("User", back_populates="plants")
    zip_code = sqlalchemy.orm.relationship("ZipCode", uselist=False)


class User(db.Model):
    """A user that owns one or more plants."""

    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    plants = sqlalchemy.orm.relationship("Plant", back_populates="user")
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    @staticmethod
    def from_json(json_input):
        """
        Convert the JSON object to a User object.

        :param dict json_input: the JSON input representing the User object
        :return: the User object based on the JSON input
        :rtype: User
        :raises ValidationError: if the input is invalid or the user already exists
        """
        User.validate_json(json_input)

        if db.session.query(User).filter_by(username=json_input["username"]).count():
            raise ValidationError(f'The user "{json_input["username"]}" already exists')

        password = bcrypt.hashpw(json_input["password"].encode("utf-8"), bcrypt.gensalt())
        return User(password=password, username=json_input["username"])

    def to_json(self):
        """
        Serialize the User object.

        :return: the JSON object representing the user
        :rtype: dict
        """
        return {"username": self.username}

    @staticmethod
    def validate_json(json_input):
        """
        Validate the input JSON.

        :param dict json_input: the JSON input representing the User object
        :raises ValidationError: if the input is invalid
        """
        invalid_exception = ValidationError(
            "The input JSON must only contain the following keys with string values: password and "
            "username"
        )
        if not isinstance(json_input, dict):
            raise invalid_exception
        elif json_input.keys() != {"password", "username"}:
            raise invalid_exception

        for value in json_input.values():
            if not isinstance(value, str):
                raise invalid_exception

    def validate_password(self, input_password):
        """
        Validate the input password.

        :param str input_password: the password provided by the user
        :raises werkzeug.exceptions.Unauthorized: if the password is incorrect
        """
        if not bcrypt.checkpw(input_password.encode("utf-8"), self.password):
            raise Unauthorized("The username or password was incorrect. Please try again.")


class ZipCode(db.Model):
    """A zip code representing a location for a plant."""

    __tablename__ = "zip_codes"
    coordinates = sqlalchemy.Column(sqlalchemy.String)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    zip_code = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False, unique=True)
