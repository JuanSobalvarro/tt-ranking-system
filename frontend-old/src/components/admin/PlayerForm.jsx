import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCountryChoices } from "services/api.js";
import { Button, Label, Select, TextInput, FileInput, Card } from "flowbite-react";

function PlayerForm({ initialData, handleSubmit }) {
  const [formData, setFormData] = useState(initialData);
  const [countryChoices, setCountryChoices] = useState([]);
  const [photoPreview, setPhotoPreview] = useState(initialData.photo ? initialData.photo : null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCountryChoices = async () => {
      try {
        const choices = await getCountryChoices();
        setCountryChoices(choices);
      } catch (error) {
        console.error("Error fetching country choices:", error);
      }
    };

    fetchCountryChoices();
  }, []);

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === "photo") {
      const file = files[0];
      if (file) {
        setFormData({ ...formData, photo: file });
        setPhotoPreview(URL.createObjectURL(file));
      }
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const onSubmit = (e) => {
  e.preventDefault();

  const dataToSubmit = { ...formData };

  // If the photo was not changed, remove it from the submission
  if (!formData.photo || formData.photo === initialData.photo) {
    delete dataToSubmit.photo;
  }

  // // Use FormData to handle file uploads
  // const formDataObject = new FormData();
  // Object.entries(dataToSubmit).forEach(([key, value]) => {
  //   formDataObject.append(key, value);
  // });

  handleSubmit(dataToSubmit);
};


  return (
    <Card>
      <form onSubmit={onSubmit} className="flex flex-col gap-4" encType="multipart/form-data">
        {/* First Name */}
        <div>
          <Label htmlFor="first_name" value="Nombre" />
          <TextInput
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Last Name */}
        <div>
          <Label htmlFor="last_name" value="Apellido" />
          <TextInput
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Alias */}
        <div>
          <Label htmlFor="alias" value="Alias (Opcional)" />
          <TextInput id="alias" name="alias" value={formData.alias} onChange={handleChange} />
        </div>

        {/* Gender */}
        <div>
          <Label htmlFor="gender" value="Género" />
          <Select id="gender" name="gender" value={formData.gender} onChange={handleChange} required>
            <option value="">Seleccione</option>
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
          </Select>
        </div>

        {/* Date of Birth */}
        <div>
          <Label htmlFor="date_of_birth" value="Fecha de nacimiento" />
          <TextInput
            id="date_of_birth"
            name="date_of_birth"
            type="date"
            value={formData.date_of_birth}
            onChange={handleChange}
            required
          />
        </div>

        {/* Nationality */}
        <div>
          <Label htmlFor="nationality" value="Nacionalidad" />
          <Select id="nationality" name="nationality" value={formData.nationality} onChange={handleChange} required>
            <option value="">Seleccione</option>
            {countryChoices.map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </Select>
        </div>

        {/* Photo Upload */}
        <div>
          <Label htmlFor="photo" value="Foto" />
          <FileInput id="photo" name="photo" accept="image/*" onChange={handleChange} />
          {photoPreview && (
            <img src={photoPreview} alt="Vista previa de la foto" className="mt-4 w-32 h-32 object-cover rounded-lg shadow" />
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-between mt-6">
          <Button type="submit" color="success">
            Guardar
          </Button>
          <Button color="gray" onClick={() => navigate("/admin/players")}>
            Cancelar
          </Button>
        </div>
      </form>
    </Card>
  );
}

export default PlayerForm;
