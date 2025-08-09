import Button from "../../components/ui/Button/Button";
import Footer from "../../components/ui/Footer/Footer";
import "./Contact.css";
import TextField from "@mui/material/TextField";
import { useForm } from "react-hook-form";
import emailjs from "@emailjs/browser";
import Snackbar from "@mui/material/Snackbar";
import { useState } from "react";
import Alert from "@mui/material/Alert";
import Typography from "@mui/material/Typography";

function Contact() {
  const { register, handleSubmit, formState, reset } = useForm();
  const { errors } = formState;

  // settings for send success or failure
  const [isNotifOpen, setNotifOpen] = useState(false);
  const [notifMsg, setNotifMsg] = useState("");
  const [notifSeverity, setNotifSeverity] = useState("success");

  const handleClose = (event, reason) => {
    setNotifOpen(false);
  };

  const sendEmail = ({ yourName, yourEmail, specSubject, msg }) => {
    const templateParams = {
      from_name: yourName,
      from_email: yourEmail,
      subject: specSubject,
      message: msg,
    };
    console.log(templateParams);

    emailjs
      .send("service_asumvkd", "template_kf8b4zr", templateParams, {
        publicKey: "2s3M43dKJ7I3v2XDT",
      })
      .then(
        (result) => {
          reset();
          setNotifOpen(true);
          setNotifMsg("Sent!");
          setNotifSeverity("success");
        },
        (error) => {
          setNotifOpen(true);
          setNotifMsg("Failed to send. Please try again.");
          setNotifSeverity("error");
        }
      );
  };

  // styles for the form
  const fieldStyle = {
    zIndex: "1",
    input: { background: "rgba(245, 244, 244, 0.80);" },
    "& .MuiOutlinedInput-root": {
      "&.Mui-focused fieldset": {
        borderColor: "#5c8080", // Outline border color on focus
      },
    },
    "& label.Mui-focused": {
      color: "#5c8080", // Label color on focus
    },
  };
  const shrinkLabel = { inputLabel: { shrink: true } };

  return (
    <div className='contact-page'>
      <div className='title-desc'>
        <h1 className='contact-title'>Contact Us</h1>
        <p className='desc'>
          We'd love to answer any questions and hear any feedback you may have.
        </p>
      </div>
      <section className='main-contact'>
        <form
          onSubmit={handleSubmit(sendEmail)}
          noValidate
        >
          <div className='form-container'>
            <TextField
              fullWidth
              name='yourName'
              label='Your Name'
              variant='outlined'
              placeholder='Enter your name'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              {...register("yourName")}
            />
            <TextField
              fullWidth
              name='email'
              label='Your email'
              variant='outlined'
              placeholder='Enter your email'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              type='email'
              {...register("yourEmail", {
                required: "Email is required",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Invalid email address",
                },
              })}
              error={!!errors.yourEmail}
            />
            {/* user did not fill in email */}
            {errors.yourEmail && (
              <Typography
                variant='caption'
                color='error'
                sx={{ mt: -3, mb: -2, width: "100%" }}
              >
                {errors.yourEmail.message}
              </Typography>
            )}
            <TextField
              fullWidth
              name='subject'
              label='Subject'
              variant='outlined'
              placeholder='Enter topic of message'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              {...register("specSubject")}
            />
            <TextField
              className='msg-input'
              fullWidth
              name='message'
              label='Message'
              multiline // textarea element rendered instead of input
              rows={5}
              placeholder='Type your questions/feedback here'
              slotProps={shrinkLabel}
              sx={{
                "& .MuiOutlinedInput-root": {
                  "&.Mui-focused fieldset": {
                    borderColor: "#5c8080", // Outline border color on focus
                  },
                },
                "& label.Mui-focused": {
                  color: "#5c8080", // Label color on focus
                },
              }}
              {...register("msg", {
                required: "Message is required",
              })}
              error={!!errors.msg}
            />
            {/* user did not fill in message */}
            {errors.msg && (
              <Typography
                variant='caption'
                color='error'
                sx={{ mt: -3, mb: -2, width: "100%" }}
              >
                {errors.msg.message}
              </Typography>
            )}
            <Button
              type='submit'
              text='Send'
            />
          </div>
        </form>
        <Snackbar
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          open={isNotifOpen}
          autoHideDuration={3000}
          onClose={handleClose}
        >
          <Alert severity={notifSeverity}>{notifMsg}</Alert>
        </Snackbar>
      </section>
      <Footer />
    </div>
  );
}
export default Contact;
