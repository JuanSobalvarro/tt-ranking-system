import React, { useState, useEffect } from "react";
import { Button, TextInput, Label, Textarea, Datepicker } from "flowbite-react";
import AlertModal from "./AlertModal";

function SeasonForm({ initialData, onSubmit, submitText }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    start_date: new Date(),
    end_date: new Date(),
    singles_points_for_win: "",
    singles_points_for_loss: "",
    doubles_points_for_win: "",
    doubles_points_for_loss: "",
  });

  useEffect(() => {
    if (initialData) {
      setFormData((prevData) => ({
        ...prevData,
        ...initialData,
        start_date: initialData.start_date ? new Date(initialData.start_date) : new Date(),
        end_date: initialData.end_date ? new Date(initialData.end_date) : new Date(),
      }));
    }
  }, [initialData]);

  const [modal, setModal] = useState({
    isOpen: false,
    type: "error",
    message: "",
  });

  const handleCloseModal = () => setModal({ isOpen: false, type: "error", message: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleDateChange = (name, date) => {
    setFormData((prevData) => ({
      ...prevData,
      [name]: date,
    }));
  };

  const validateForm = () => {
    let errors = [];

    if (!formData.name) errors.push("El nombre de la temporada es requerido.");
    if (!formData.start_date) errors.push("La fecha de inicio es requerida.");
    if (!formData.end_date) errors.push("La fecha de fin es requerida.");
    if (formData.start_date > formData.end_date) errors.push("La fecha de inicio no puede ser mayor que la fecha de fin.");

    return errors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validateForm();

    if (validationErrors.length > 0) {
      setModal({
        isOpen: true,
        type: "error",
        message: validationErrors.join("\n"),
      });
      return;
    }

    setModal({
      isOpen: true,
      type: "success",
      message: "Temporada guardada exitosamente.",
    });

    onSubmit({
      ...formData,
      start_date: formData.start_date.toISOString().split("T")[0],
      end_date: formData.end_date.toISOString().split("T")[0],
      singles_points_for_win: Number(formData.singles_points_for_win),
      singles_points_for_loss: Number(formData.singles_points_for_loss),
      doubles_points_for_win: Number(formData.doubles_points_for_win),
      doubles_points_for_loss: Number(formData.doubles_points_for_loss),
    });
  };

  return (
    <>
      <AlertModal isOpen={modal.isOpen} onClose={handleCloseModal} type={modal.type} message={modal.message} />

      <form onSubmit={handleSubmit} className="space-y-6 max-w-xl mx-auto">
        <div>
          <Label htmlFor="name" value="Nombre de la Temporada" />
          <TextInput id="name" name="name" value={formData.name} onChange={handleChange} type="text" required />
        </div>

        <div>
          <Label htmlFor="description" value="Descripción" />
          <Textarea id="description" name="description" value={formData.description} onChange={handleChange} placeholder="Descripción opcional" />
        </div>

        <div>
          <Label htmlFor="start_date" value="Fecha de Inicio" />
          <Datepicker id="start_date" name="start_date" value={formData.start_date} onChange={(date) => handleDateChange("start_date", date)} required />
        </div>

        <div>
          <Label htmlFor="end_date" value="Fecha de Fin" />
          <Datepicker id="end_date" name="end_date" value={formData.end_date} onChange={(date) => handleDateChange("end_date", date)} required />
        </div>

        <div>
          <Label htmlFor="singles_points_for_win" value="Puntos para ganar en Singles" />
          <TextInput id="singles_points_for_win" name="singles_points_for_win" value={formData.singles_points_for_win} onChange={handleChange} type="number" />
        </div>

        <div>
          <Label htmlFor="singles_points_for_loss" value="Puntos para perder en Singles" />
          <TextInput id="singles_points_for_loss" name="singles_points_for_loss" value={formData.singles_points_for_loss} onChange={handleChange} type="number" />
        </div>

        <div>
          <Label htmlFor="doubles_points_for_win" value="Puntos para ganar en Dobles" />
          <TextInput id="doubles_points_for_win" name="doubles_points_for_win" value={formData.doubles_points_for_win} onChange={handleChange} type="number" />
        </div>

        <div>
          <Label htmlFor="doubles_points_for_loss" value="Puntos para perder en Dobles" />
          <TextInput id="doubles_points_for_loss" name="doubles_points_for_loss" value={formData.doubles_points_for_loss} onChange={handleChange} type="number" />
        </div>

        <div className="text-center">
          <Button type="submit" className="bg-blue-600 hover:bg-blue-700 w-full py-2 text-white">
            {submitText}
          </Button>
        </div>
      </form>
    </>
  );
}

export default SeasonForm;
