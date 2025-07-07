import React from "react";
import { Modal, Button } from "flowbite-react";

function ConfirmationModal({ isOpen, onConfirm, onCancel, message = "Are you sure you want to delete this item?",
                           deleteItem = "Borrar", cancelItem = "Cancelar" }) {
  return (
    <Modal
      show={isOpen}
      size="md"
      popup={true}
      onClose={onCancel}
      className="backdrop-blur-sm"
    >
      <Modal.Header />
      <Modal.Body>
        <div className="text-center">
          <h3 className="text-lg font-medium text-gray-900">{message}</h3>
          <div className="mt-5 flex justify-center gap-4">
            <Button
              color="failure"
              onClick={onConfirm}
              className="bg-red-600 hover:bg-red-700"
            >
                {deleteItem}
            </Button>
            <Button
              color="gray"
              onClick={onCancel}
              className="bg-gray-300 hover:bg-gray-400"
            >
                {cancelItem}
            </Button>
          </div>
        </div>
      </Modal.Body>
    </Modal>
  );
}

export default ConfirmationModal;
